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
import registry

# Воркер для сбора данных
class CollectWorker(QThread):
    def __init__(self, config, data_lists):
        super().__init__()

        self.collect_interval = config.getCollectInterval()
        self.config = config
        self.data_lists = data_lists

    result = pyqtSignal(dict, bool)

    def run(self):
        self.keepRunning = True
        while self.keepRunning:
            data = hardware.collectData(self.data_lists)

            if not self.config.getIsCPUManagmentOn():
                CPU_performance_mode = True
            else:
                CPU_performance_mode = hardware.setCpuPerformanceState(self.config, self.data_lists)

            self.result.emit(data, CPU_performance_mode)
            time.sleep(self.collect_interval)

    def update(self, config):
        self.collect_interval = config.getCollectInterval()
        self.config = config

    def stop(self):
        self.keepRunning = False

# Воркер для бэкапа данных
class BackupWorker(QThread):
    def __init__(self, backup_interval):
        super().__init__()

        self.backup_interval = backup_interval

    result = pyqtSignal(bool)

    def run(self):
        self.keepRunning = True
        while self.keepRunning:
            time.sleep(self.backup_interval)
            self.result.emit(True)

    def update(self, backup_interval):
        self.backup_interval = backup_interval

    def stop(self):
        self.keepRunning = False

# Воркер для мониторинга системных параметров
class SystemMonitoringWorker(QThread):
    def __init__(self, system_data_collect_interval):
        super().__init__()

        self.system_data_collect_interval = system_data_collect_interval

    result = pyqtSignal(dict)

    def run(self):
        self.keepRunning = True
        while self.keepRunning:

            time.sleep(self.system_data_collect_interval)
            data = {
                    'system_uses_light_theme' : registry.getCurrentThemeIsLight()
                    }

            self.result.emit(data)

    def update(self, system_data_collect_interval):
        self.system_data_collect_interval = system_data_collect_interval

    def stop(self):
        self.keepRunning = False

class Main(QMainWindow,  windows.mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Дизайн

        #Прочитаем конфиг
        self.config = Entities.Config()

        #Прочитаем статус турбо
        self.turbo_statuses = Entities.TurboStatuses()

        support.readConfig(self)

        #Листы для хранения данных
        self.data_lists = {
                        'general_temps' : [], 
                        'average_temps' : [],
                        'general_tdp' : [],
                        'average_tdp' : [],
                        'all_load' : [],
                    }

        if self.config.getIsBackupNeeded():
            if support.getRestoredData():
                self.data_lists = support.getRestoredData()

            #Интервал для сохранения данных на диск
            self.backup_interval = self.config.getBackupInterval()

            self.startBackupWorker()

        self.startSystemMonitoringWorker()

        if self.config.getIsCPUManagmentOn():
            CPU_performance_mode = hardware.setCpuPerformanceState(self.config, self.data_lists)
            self.config.setPerformanceCPUModeOn(CPU_performance_mode)

        data = hardware.collectData(self.data_lists)

        self.cpu_cores = len(data['cpu']['cores'])
        self.cpu_threads = len(data['cpu']['threads'])

        #Есть ли HT/SMT
        if self.cpu_cores != self.cpu_threads:
            self.SMT = True
        else:
            self.SMT = False

        #Проставим размер таблицы для проца
        self.CPUinfoTable.setRowCount(self.cpu_cores)
 
        self.image = support.getTrayImage(0, self.config)

        #За сколько секунд храним данные, 86400 — сутки
        self.store_period = self.config.getStorePeriod()

        #Интервал сбора
        self.collect_interval = self.config.getCollectInterval()

        #А это коэффициент, зависящий от сбора, чтобы вне зависимости от частоты сбора, 
        #мы всегда брали столько показаний, сколько нужно для временных рамок.
        #Условно, нам надо брать за минуту, то частота сбора 0.5, тогда из листов мы будем брать не 60 показаний
        #А 60*2, где 2 — self.collect_interval
        self.collect_koef = round(1/self.collect_interval)

        #Проставим название проца
        self.setCpuName()

        #Зададим размеры окошка исходя из оборудования
        self.setWindowsSizes()

        #Обработка кнопок
        self.buttonResetGeneralTemps.clicked.connect(self.resetGeneralTemps)
        self.buttonResetTDP.clicked.connect(self.resetTDP)
        self.buttonResetAverageTemps.clicked.connect(self.resetAverage)
        self.buttonShowSettings.clicked.connect(self.showSettings)

        self.startCollectWorker()

        #Плашка если нет админских прав
        if support.isThereAdminRight():
            self.frameAdminRight.setVisible(False)

    #Перезаписываем событие не закрытие, чтобы скрывать в трей если это надо
    def closeEvent(self, event):
        if self.config.getCloseToTray():
            event.ignore()
            self.hide()
        else:
            #Иначе вернем лимиты проца по умолчанию — 100
            hardware.setCPUStatetoDefault()
            hardware.setTurboToDefault()

    def startCollectWorker(self):
        #Создаем воркер для сбора и обновления информации
        self.collect_worker = CollectWorker(self.config, self.data_lists)
        self.collect_worker.result.connect(self.processData)
        self.collect_worker.start()

    def startBackupWorker(self):
        #Создаем воркер для бэкапа данных
        self.backup_worker = BackupWorker(self.backup_interval)
        self.backup_worker.result.connect(self.saveData)
        self.backup_worker.start()

    def startSystemMonitoringWorker(self):
        #Создаем воркер для мониторинга системных параметров
        self.system_monitoring_worker = SystemMonitoringWorker(self.config.getSystemDataCollectIntreval())
        self.system_monitoring_worker.result.connect(self.updateSystemStateConfig)
        self.system_monitoring_worker.start()

    #Функции для сбора записанных данных
    def resetGeneralTemps(self):
        self.data_lists['general_temps'] = []

    def resetTDP(self):
         self.data_lists['general_tdp'] = []

    def resetAverage(self):
        self.data_lists['average_temps'] = []
        self.data_lists['average_tdp'] = []

    def resetAllData(self):
        self.resetGeneralTemps()
        self.resetTDP()
        self.resetAverage()

    def setCpuName(self):
        cpu_name = hardware.getCpuName()
        cpu_name_with_counts = cpu_name + ' (' + str(self.cpu_cores) + '/' + str(self.cpu_threads) + ')'
        self.cpuNameLabel.setText(cpu_name_with_counts)

    def setWindowsSizes(self):
        additional_cpu_cores_height = (self.cpu_cores - 6) * 24

        self.resize(400, 330 + additional_cpu_cores_height)

    def getAvgTempForSeconds(self, collect_interval):
        average_temps_sum_perion = sum(self.data_lists['average_temps'][:collect_interval*self.collect_koef])
        average_temps_len_perion = len(self.data_lists['average_temps'][:collect_interval*self.collect_koef])

        return average_temps_sum_perion/average_temps_len_perion

    def getAvgTDPForSeconds(self, collect_interval):
        average_tdps_sum_perion = sum(self.data_lists['average_tdp'][:collect_interval*self.collect_koef])
        average_tdps_len_perion = len(self.data_lists['average_tdp'][:collect_interval*self.collect_koef])

        return average_tdps_sum_perion/average_tdps_len_perion

    #Записываем данные
    def writeData(self, result):        
        #Записываем значения
        if round(result['cpu']['temp'], 1) > 0:
            self.data_lists['general_temps'].insert(0, result['cpu']['temp'])
            self.data_lists['average_temps'].insert(0, result['cpu']['temp'])
        
        if round(result['cpu']['tdp'], 1) > 0 and result['cpu']['tdp'] != inf:
            self.data_lists['general_tdp'].insert(0, result['cpu']['tdp'])
            self.data_lists['average_tdp'].insert(0, result['cpu']['tdp'])

        if round(result['all_load'], 1) > 0 and result['all_load'] != inf:
            self.data_lists['all_load'].insert(0, result['all_load'])

        #Обрезаем массивы
        self.data_lists['general_temps'] = self.data_lists['general_temps'][:self.store_period]
        self.data_lists['average_temps'] = self.data_lists['average_temps'][:self.store_period]
        self.data_lists['general_tdp'] = self.data_lists['general_tdp'][:self.store_period]
        self.data_lists['all_load'] = self.data_lists['all_load'][:self.store_period]

    #Обработка данных из collectWorker'а
    def processData(self, result, CPU_performance_mode):
        if result['status'] in (Entities.Status.error, Entities.Status.not_collect):
            return

        self.config.setPerformanceCPUModeOn(CPU_performance_mode)

        self.writeData(result)
        
        if len(self.data_lists['general_temps']) > 0:
            #Минимальная
            min_temp = support.toRoundStr(min(self.data_lists['general_temps']))
            self.lineEditCpuMinTemp.setText(min_temp)

            #Текущая
            current_temp = support.toRoundStr(self.data_lists['general_temps'][:1][0])
            self.lineEditCpuCurrentTemp.setText(current_temp)

            self.image = support.getTrayImage(current_temp, self.config)

            #Максимальная
            max_temp = support.toRoundStr((max(self.data_lists['general_temps'])))
            self.lineEditCpuMaxTemp.setText(max_temp)
        else:
            self.lineEditCpuMinTemp.setDisabled(True)
            self.lineEditCpuCurrentTemp.setDisabled(True)
            self.lineEditCpuMaxTemp.setDisabled(True)
            self.buttonResetGeneralTemps.setDisabled(True)

        if len(self.data_lists['general_tdp']) > 0:
            #Минимальный
            min_tdp = support.toRoundStr(min(self.data_lists['general_tdp']))
            self.lineEditCpuMinTDP.setText(min_tdp)

            #Текущий
            current_tdp = support.toRoundStr(self.data_lists['general_tdp'][:1][0])
            self.lineEditCpuCurrentTDP.setText(current_tdp)

            #Максимальный
            max_tdp = support.toRoundStr((max(self.data_lists['general_tdp'])))
            self.lineEditCpuMaxTDP.setText(max_tdp)
        else:
            self.lineEditCpuMinTDP.setDisabled(True)
            self.lineEditCpuCurrentTDP.setDisabled(True)
            self.lineEditCpuMaxTDP.setDisabled(True)
            self.buttonResetTDP.setDisabled(True)

        if len(self.data_lists['average_temps']) > 0:

            row = 0

            for minutes in (1, 5, 15, 60, 60*24):
                avg_temp = support.toRoundStr(self.getAvgTempForSeconds(60*minutes))
                avg_tdp = support.toRoundStr(self.getAvgTDPForSeconds(60*minutes))

                self.tableAverage.setItem(row, 0, QTableWidgetItem(avg_temp + ' С°'))
                self.tableAverage.setItem(row, 1, QTableWidgetItem(avg_tdp + ' Вт'))

                row += 1

        else:
            self.tableAverage.setDisabled(True)

        for core in result['cpu']['cores']:
            if 'clock' in core:
                self.CPUinfoTable.setItem(int(core['id'])-1 , 0, QTableWidgetItem(str(core['clock'])))

                if self.SMT:
                    avg_load_by_core = support.toRoundStr((
                                                        result['cpu']['threads'][(core['id']-1)*2]['load'] + 
                                                        result['cpu']['threads'][(core['id']-1)*2-1]['load']
                                                        )/2)
                else:
                    avg_load_by_core = support.toRoundStr(result['cpu']['threads'][(core['id']-1)])

                self.CPUinfoTable.setItem(int(core['id'])-1 , 1, QTableWidgetItem(avg_load_by_core + '%'))

    #Обработка данных из backupWorker'а
    def saveData(self):
        support.saveData(self.data_lists)

    #Обработка данных из SystemMonitoringWorker'а
    def updateSystemStateConfig(self, data):
        self.config.setSystemUsesLightTheme(data['system_uses_light_theme'])

        support.writeToConfig(self.config)
        new_config = support.readConfig(self)

        self.collect_worker.update(new_config)

    def showSettings(self):
        window = SettingsWindow.Main()        
        app_icon = support.getResourcePath('./images/icon.png')

        window.setWindowIcon(QIcon(app_icon))

        window.setData(self.config, self.turbo_statuses)

        if window.exec():
            #Обновим воркеры, пока мы еще можем сравнивать состояния
            if self.config.getIsBackupNeeded() and not window.config.getIsBackupNeeded():
                self.backup_worker.stop()
                support.removeStatFile()
            
            if not self.config.getIsBackupNeeded() and window.config.getIsBackupNeeded():
                self.startBackupWorker()

            #Позаботимся обновить ограничения процессора если они поменялись
            if self.config.getIsCPUManagmentOn():
                hardware.updateCPUParameters(self.config, 
                                             window.config.getCPUIdleState(), 
                                             window.config.getCPULoadState(),
                                             window.config.getCPUTurboIdleId(),
                                             window.config.getCPUTurboLoadId()
                                             )
            
            #И если пользователь отключил управление процом — выставим все в сотку и турбо без ограничений, обычно это дефолт
            if window.config.getIsCPUManagmentOn() == False and (window.config.getIsCPUManagmentOn() != self.config.getIsCPUManagmentOn()):
                hardware.setCPUStatetoDefault()
                hardware.setTurboToDefault()

            #Обновим конфиг и перечитаем его
            support.writeToConfig(window.config)
            new_config = support.readConfig(self)

            self.collect_worker.update(new_config)