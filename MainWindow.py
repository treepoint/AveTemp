from math import inf
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt6.QtCore import QThread, pyqtSignal
import time

import SettingsWindow

import hardware
import Entities
import support

# Воркер для сбора данных
class Worker(QThread):
    def __init__(self, collect_interval):
        super().__init__()

        self.collect_interval = collect_interval

    result = pyqtSignal(dict)

    def run(self):
        self.keepRunning = True
        while self.keepRunning:
            res = hardware.collectData()
            self.result.emit(res)
            time.sleep(self.collect_interval)

    def update(self, collect_interval):
        self.collect_interval = collect_interval

    def stop(self):
        self.keepRunning = False

class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('windows/main.ui', self)

        #Листы для хранения данных
        self.general_temps = []
        self.average_temps = []
        self.tdp = []

        # прочитаем конфиг
        self.config = Entities.Config()

        support.readConfig(self)
        
        self.image = support.get_tray_image(0)

        #За сколько секунд храним данные, 86400 — сутки
        self.store_period = self.config.get_store_period()

        #Период сбора
        self.collect_interval = self.config.get_collect_interval()

        #А это коэффициент, зависящий от сбора, чтобы вне зависимости от частоты сбора, 
        #мы всегда брали столько показаний, сколько нужно для временных рамок.
        #Условно, нам надо брать за минуту, то частота сбора 0.5, тогда из листов мы будем брать не 60 показаний
        #А 60*2, где 2 — self.collect_interval
        self.collect_koef = round(1/self.collect_interval)

        #Проставим название проца
        self.set_cpu_name()

        #Обработка кнопок
        self.buttonResetGeneralTemps.clicked.connect(self.reset_general_temps)
        self.buttonResetTDP.clicked.connect(self.reset_tdp)
        self.buttonResetAverageTemps.clicked.connect(self.reset_average_temps)
        self.buttonShowSettings.clicked.connect(self.showSettings)

        self.start_worker()

        #Плашка если нет админских прав
        if support.check_admin_right():
            self.frameAdminRight.setVisible(False)

    #Перезаписываем событие не закрытие, чтобы скрывать в трей если это надо
    def closeEvent(self, event):
        if self.config.get_close_to_tray():
            event.ignore()
            self.hide()

    def start_worker(self):
        #Создаем воркер для сбора и обновления информации
        self.worker = Worker(self.collect_interval)
        self.worker.result.connect(self.process_data)
        self.worker.start()

    #Функции для сбора записанных данных
    def reset_general_temps(self):
        self.general_temps = []

    def reset_tdp(self):
        self.tdp = []

    def reset_average_temps(self):
        self.average_temps = []

    def reset_all_data(self):
        self.reset_general_temps()
        self.reset_tdp()
        self.reset_average_temps()

    def set_cpu_name(self):
        cpu_name = hardware.getCpuName()
        self.cpuNameLabel.setText(cpu_name)

    def get_avg_temp_for_seconds(self, collect_interval):
        average_temps_sum_perion = sum(self.average_temps[:collect_interval*self.collect_koef])
        average_temps_len_perion = len(self.average_temps[:collect_interval*self.collect_koef])

        return average_temps_sum_perion/average_temps_len_perion

    #Записываем данные
    def write_data(self, result):
        #Записываем значения
        if result['cpu']['temp'] > 0:
            self.general_temps.insert(0, result['cpu']['temp'])
            self.average_temps.insert(0, result['cpu']['temp'])
        
        if result['cpu']['tdp'] > 0 and result['cpu']['tdp'] != inf:
            self.tdp.insert(0, result['cpu']['tdp'])

        #Обрезаем массивы
        self.general_temps = self.general_temps[:self.store_period]
        self.average_temps = self.average_temps[:self.store_period]
        self.tdp = self.tdp[:self.store_period]

    #Обработка данных из worker'а
    def process_data(self, result):
        if result['status'] in (Entities.Status.error, Entities.Status.not_collect):
            return

        self.write_data(result)
        
        if len(self.general_temps) > 0:
            #Минимальная
            min_temp = support.to_round_str(min(self.general_temps))
            self.lineEditCpuMinTemp.setText(min_temp)

            #Текущая
            current_temp = support.to_round_str(self.general_temps[:1][0])
            self.lineEditCpuCurrentTemp.setText(current_temp)

            self.image = support.get_tray_image(current_temp)

            #Максимальная
            max_temp = support.to_round_str((max(self.general_temps)))
            self.lineEditCpuMaxTemp.setText(max_temp)
        else:
            self.lineEditCpuMinTemp.setDisabled(True)
            self.lineEditCpuCurrentTemp.setDisabled(True)
            self.lineEditCpuMaxTemp.setDisabled(True)
            self.buttonResetGeneralTemps.setDisabled(True)

        if len(self.tdp) > 0:
            #Минимальный
            min_tdp = support.to_round_str(min(self.tdp))
            self.lineEditCpuMinTDP.setText(min_tdp)

            #Текущий
            current_tdp = support.to_round_str(self.tdp[:1][0])
            self.lineEditCpuCurrentTDP.setText(current_tdp)

            #Максимальный
            max_tdp = support.to_round_str((max(self.tdp)))
            self.lineEditCpuMaxTDP.setText(max_tdp)
        else:
            self.lineEditCpuMinTDP.setDisabled(True)
            self.lineEditCpuCurrentTDP.setDisabled(True)
            self.lineEditCpuMaxTDP.setDisabled(True)
            self.buttonResetTDP.setDisabled(True)

        if len(self.average_temps) > 0:
            #За 1 минуту. Да здесь можно было бы в цикле, но у нас пока всего 5 статичных полей — не требуется лишняя сложность
            one_minute_avg_temp = support.to_round_str(self.get_avg_temp_for_seconds(60))
            self.lineEditCpu1minTemp.setText(one_minute_avg_temp)

            #За 5 минут
            five_minutes_avg_temp = support.to_round_str(self.get_avg_temp_for_seconds(60*5))
            self.lineEditCpu5minTemp.setText(five_minutes_avg_temp)

            #За 15 минут
            fifteen_minutes_avg_temp = support.to_round_str(self.get_avg_temp_for_seconds(60*15))
            self.lineEditCpu15minTemp.setText(fifteen_minutes_avg_temp)

            #За 1 час
            one_hour_avg_temp = support.to_round_str(self.get_avg_temp_for_seconds(60*60))
            self.lineEditCpu1hourTemp.setText(one_hour_avg_temp)

            #За 24 часа
            twenty_four_hour_avg_temp = support.to_round_str(self.get_avg_temp_for_seconds(60*60*24))
            self.lineEditCpu24hourTemp.setText(twenty_four_hour_avg_temp)
        else:
            self.lineEditCpu1minTemp.setDisabled(True)
            self.lineEditCpu5minTemp.setDisabled(True)
            self.lineEditCpu15minTemp.setDisabled(True)
            self.lineEditCpu1hourTemp.setDisabled(True)
            self.lineEditCpu24hourTemp.setDisabled(True)
            self.buttonResetAverageTemps.setDisabled(True)

        #Реализуем таблицу с частотами и загрузкой процессора
        self.CPUinfoTable.setRowCount(len(result['cpu']['cores']))

        for core in result['cpu']['cores']:
            if 'clock' in core:
                self.CPUinfoTable.setItem(int(core['id'])-1 , 0, QTableWidgetItem(str(core['clock'])))

                avg_by_core = support.to_round_str((result['cpu']['threads'][(core['id']-1)*2]['load']+result['cpu']['threads'][(core['id']-1)*2-1]['load'])/2)

                self.CPUinfoTable.setItem(int(core['id'])-1 , 1, QTableWidgetItem(avg_by_core + '%'))

    def showSettings(self):
        window = SettingsWindow.Main()
        window.setData(self.config)

        if window.exec():
            support.writeToConfig(self, window.config)
            support.readConfig(self)

            self.worker.update(self.config.get_collect_interval())