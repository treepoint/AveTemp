from math import inf
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt6.QtCore import QThread, pyqtSignal
import time

import SettingsWindow
import windows.mainWindow

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

class Main(QMainWindow,  windows.mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Дизайн

        #Листы для хранения данных
        self.general_temps = []
        self.average_temps = []
        self.general_tdp = []
        self.average_tdp = []

        init_data = hardware.collectData()

        self.cpu_cores = len(init_data['cpu']['cores'])
        self.cpu_threads = len(init_data['cpu']['threads'])

        #Есть ли HT/SMT
        if self.cpu_cores != self.cpu_threads:
            self.SMT = True
        else:
            self.SMT = False

        #Проставим размер таблицы для проца
        self.CPUinfoTable.setRowCount(self.cpu_cores)

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

        #Зададим размеры окошка исходя из оборудования
        self.set_windows_sizes()

        #Обработка кнопок
        self.buttonResetGeneralTemps.clicked.connect(self.reset_general_temps)
        self.buttonResetTDP.clicked.connect(self.reset_tdp)
        self.buttonResetAverageTemps.clicked.connect(self.reset_average)
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
        self.general_tdp = []

    def reset_average(self):
        self.average_temps = []
        self.average_tdp = []

    def reset_all_data(self):
        self.reset_general_temps()
        self.reset_tdp()
        self.reset_average()

    def set_cpu_name(self):
        cpu_name = hardware.getCpuName()
        cpu_name_with_counts = cpu_name + ' (' + str(self.cpu_cores) + '/' + str(self.cpu_threads) + ')'
        self.cpuNameLabel.setText(cpu_name_with_counts)

    def set_windows_sizes(self):
        additional_cpu_cores_height = (self.cpu_cores - 6) * 24

        self.resize(400, 330 + additional_cpu_cores_height)

    def get_avg_temp_for_seconds(self, collect_interval):
        average_temps_sum_perion = sum(self.average_temps[:collect_interval*self.collect_koef])
        average_temps_len_perion = len(self.average_temps[:collect_interval*self.collect_koef])

        return average_temps_sum_perion/average_temps_len_perion

    def get_avg_tdp_for_seconds(self, collect_interval):
        average_tdps_sum_perion = sum(self.average_tdp[:collect_interval*self.collect_koef])
        average_tdps_len_perion = len(self.average_tdp[:collect_interval*self.collect_koef])

        return average_tdps_sum_perion/average_tdps_len_perion

    #Записываем данные
    def write_data(self, result):
        #Записываем значения
        if round(result['cpu']['temp'], 1) > 0:
            self.general_temps.insert(0, result['cpu']['temp'])
            self.average_temps.insert(0, result['cpu']['temp'])
        
        if round(result['cpu']['tdp'], 1) > 0 and result['cpu']['tdp'] != inf:
            self.general_tdp.insert(0, result['cpu']['tdp'])
            self.average_tdp.insert(0, result['cpu']['tdp'])

        #Обрезаем массивы
        self.general_temps = self.general_temps[:self.store_period]
        self.average_temps = self.average_temps[:self.store_period]
        self.general_tdp = self.general_tdp[:self.store_period]

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

        if len(self.general_tdp) > 0:
            #Минимальный
            min_tdp = support.to_round_str(min(self.general_tdp))
            self.lineEditCpuMinTDP.setText(min_tdp)

            #Текущий
            current_tdp = support.to_round_str(self.general_tdp[:1][0])
            self.lineEditCpuCurrentTDP.setText(current_tdp)

            #Максимальный
            max_tdp = support.to_round_str((max(self.general_tdp)))
            self.lineEditCpuMaxTDP.setText(max_tdp)
        else:
            self.lineEditCpuMinTDP.setDisabled(True)
            self.lineEditCpuCurrentTDP.setDisabled(True)
            self.lineEditCpuMaxTDP.setDisabled(True)
            self.buttonResetTDP.setDisabled(True)

        if len(self.average_temps) > 0:

            row = 0

            for minutes in (1, 5, 15, 60, 60*24):
                avg_temp = support.to_round_str(self.get_avg_temp_for_seconds(60*minutes))
                avg_tdp = support.to_round_str(self.get_avg_tdp_for_seconds(60*minutes))

                self.tableAverage.setItem(row, 0, QTableWidgetItem(avg_temp + ' С°'))
                self.tableAverage.setItem(row, 1, QTableWidgetItem(avg_tdp + ' Вт'))

                row += 1

        else:
            self.tableAverage.setDisabled(True)

        for core in result['cpu']['cores']:
            if 'clock' in core:
                self.CPUinfoTable.setItem(int(core['id'])-1 , 0, QTableWidgetItem(str(core['clock'])))

                if self.SMT:
                    avg_load_by_core = support.to_round_str((
                                                        result['cpu']['threads'][(core['id']-1)*2]['load'] + 
                                                        result['cpu']['threads'][(core['id']-1)*2-1]['load']
                                                        )/2)
                else:
                    avg_load_by_core = support.to_round_str(result['cpu']['threads'][(core['id']-1)])

                self.CPUinfoTable.setItem(int(core['id'])-1 , 1, QTableWidgetItem(avg_load_by_core + '%'))

    def showSettings(self):
        window = SettingsWindow.Main()        
        app_icon = support.resource_path('./images/icon.png')

        window.setWindowIcon(QIcon(app_icon))

        window.setData(self.config)

        if window.exec():
            support.writeToConfig(self, window.config)
            support.readConfig(self)

            self.worker.update(self.config.get_collect_interval())