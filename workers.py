from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QTableWidgetItem

import time
import registry
import hardware
import system
import data
import support

import localization
import Entities

trans = localization.trans
languages = Entities.Languages()

# 
# Воркер для обновления информации в трее
# 
class TrayWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        self.collect_slow_data_interval = app_self.collect_slow_data_interval
        self.app = app_self.app

    result = pyqtSignal(bool)

    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            time.sleep(self.collect_slow_data_interval)

            if self.app.lastWindowClosed:
                self.result.emit(True)
            else:
                self.result.emit(False)

    def stop(self):
        self.keepRunning = False



# 
# Воркер для сбора данных
# 
class CollectSlowDataWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        self.collect_slow_data_interval = app_self.config.getCollectSlowDataInterval()
        self.computer = app_self.computer
        self.data_lists = app_self.data_lists

    result = pyqtSignal(dict)

    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            data = hardware.collectSlowData(self.computer, self.data_lists)
            self.result.emit(data)
            time.sleep(self.collect_slow_data_interval)

    def update(self, config):
        self.collect_slow_data_interval = config.getCollectSlowDataInterval()

    def stop(self):
        self.keepRunning = False

#Создаем воркер для сбора и обновления информации
def startCollectSlowDataWorker(self):
    self.collect_slow_worker = CollectSlowDataWorker(self)
    self.collect_slow_worker.result.connect(self.processSlowData)
    self.collect_slow_worker.start()

#Обработка данных из collectWorker'а
def processSlowData(self, result):        
    data.writeTempData(self, result)
    data.writeTDPData(self, result)
    data.writeCoresData(self, result)



# 
# Воркер для мониторинга нагрузки на CPU
# 
class CollectFastDataWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        #Задаем самый высокий приоритет, чтобы меньше пролагов было
        system.increase_current_process_priority()

        self.config = app_self.config
        self.collect_fast_data_interval = self.config.getCollectFastDataInterval()
        self.computer = app_self.computer
        self.cpu_cores = app_self.cpu_cores
        self.cpu_threads = app_self.cpu_threads
        self.data_lists = app_self.data_lists

    result = pyqtSignal(dict)

    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            data = hardware.collectFastData(self.computer, self.data_lists, self.cpu_threads)
            self.result.emit(data)
            time.sleep(self.collect_fast_data_interval)

    def stop(self):
        self.keepRunning = False

#Создаем воркер для мониторинга нагрузки на CPU
def startCollectFastDataWorker(self):
    self.collect_fast_worker = CollectFastDataWorker(self)
    self.collect_fast_worker.result.connect(self.processFastData)
    self.collect_fast_worker.start()

#Обработка данных из CollectFastDataWorker'а
def processFastData(self, result):
    if not self.config.getIsCPUManagmentOn():
        is_CPU_in_load_mode = False
    else:
        is_CPU_in_load_mode = hardware.setCpuPerformanceState(self.config, self.data_lists)

    self.config.setIsCPUinLoadMode(is_CPU_in_load_mode)

    data.writeThreadsData(self, result)


# 
# Воркер для бэкапа данных
# 
class BackupWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        self.backup_interval = int((app_self.config.getBackupInterval())*60)

    result = pyqtSignal(bool)

    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            current_interval = self.backup_interval

            for i in range(current_interval):
                if current_interval != self.backup_interval:
                    break
                else:
                    time.sleep(1)
                    
            self.result.emit(True)

    def update(self, config):
        self.backup_interval = int((config.getBackupInterval())*60)

    def stop(self):
        self.keepRunning = False

#Создаем воркер для бэкапа данных
def startBackupWorker(self):
    self.backup_worker = BackupWorker(self)
    self.backup_worker.result.connect(self.saveStatistics)
    self.backup_worker.start()

#Обработка данных из backupWorker'а
def saveStatistics(self):
    support.saveStatistics(self)



# 
# Воркер для мониторинга системных параметров
# 
class SystemMonitoringWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        self.system_data_collect_interval = app_self.config.getSystemDataCollectIntreval()

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

#Создаем воркер для мониторинга системных параметров
def startSystemMonitoringWorker(self):
    self.system_monitoring_worker = SystemMonitoringWorker(self)
    self.system_monitoring_worker.result.connect(self.updateSystemStateConfig)
    self.system_monitoring_worker.start()

#Обработка данных из SystemMonitoringWorker'а
def updateSystemStateConfig(self, data):
    self.config.setSystemUsesLightTheme(data['system_uses_light_theme'])

    support.writeToConfig(self.config)
    new_config = support.readConfig(self)

    self.collect_slow_worker.update(new_config)



# 
# Воркер для обновления показателей в интерфейсе
# 
class UpdateUiScoresWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        self.collect_slow_data_interval = app_self.config.getCollectSlowDataInterval()

    result = pyqtSignal(bool)

    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            self.result.emit(True)
            time.sleep(self.collect_slow_data_interval)

    def update(self, config):
        self.collect_slow_data_interval = config.getCollectSlowDataInterval()

    def stop(self):
        self.keepRunning = False

def startUpdateUiScoresWorker(self):
    #Создаем воркер обновления показателей интерфейса
    #У нас теперь данные стекаются с разных воркеров, так что обновлять надо централизовано
    self.update_ui_scores_worker = UpdateUiScoresWorker(self)
    self.update_ui_scores_worker.result.connect(self.updateUiScores)
    self.update_ui_scores_worker.start()

#Обработка данных из UpdateUiScoresWorker'а — обновляем показатели в интерфейсе
def updateUiScores(self, result):

    data_lists = self.data_lists
    
    if len(data_lists['general_temps']) > 0:
        #Минимальная
        self.lineEditCpuMinTemp.setText(str(data_lists['min_temp']))
        #Текущая
        self.lineEditCpuCurrentTemp.setText(str(data_lists['current_temp']))
        #Максимальная
        self.lineEditCpuMaxTemp.setText(str(data_lists['max_temp']))

    if len(data_lists['general_TDP']) > 0:
        #Минимальный
        self.lineEditCpuMinTDP.setText(str(data_lists['min_TDP']))
        #Текущий
        self.lineEditCpuCurrentTDP.setText(str(data_lists['current_TDP']))
        #Максимальный
        self.lineEditCpuMaxTDP.setText(str(data_lists['max_TDP']))

    if len(data_lists['average_temps']) > 0:

        row = 0

        for minutes in (1, 5, 15, 60, 60*24):
            avg_temp = support.toRoundStr(hardware.getAvgTempForSeconds(self, 60*minutes))
            avg_tdp = support.toRoundStr(hardware.getAvgTDPForSeconds(self, 60*minutes))

            self.tableAverage.setItem(row, 0, QTableWidgetItem(f"{ avg_temp } С°"))            
            self.tableAverage.setItem(row, 1, QTableWidgetItem(f"{ avg_tdp } { trans(self.locale, 'watt') }"))

            row += 1

    for core in self.data_lists['cpu']['cores']:
        self.CPUinfoTable.setItem(core['id'], 0, QTableWidgetItem(core['clock']))

    #Идем по физическим ядрам, потому что нам надо сопоставить нагрузку между потоками и ядрами   
    for index, thread in enumerate(data_lists['cpu']['threads']):
        if self.SMT:
            load = support.toRoundStr((
                                        float(data_lists['cpu']['threads'][(thread['id']-1)*2]['load']) + 
                                        float(data_lists['cpu']['threads'][(thread['id']-1)*2-1]['load'])
                                        )/2)
        else:
            load = str(thread['load'])

        self.CPUinfoTable.setItem(thread['id'], 1, QTableWidgetItem(f"{ load }%"))

        if self.SMT and index + 1 == (self.cpu_threads/2):
            break


# 
# Воркер для обновления изображения в трее
# 
class UpdateTrayIconWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        self.collect_slow_data_interval = app_self.config.getCollectSlowDataInterval()

    result = pyqtSignal(bool)

    def run(self):
        self.keepRunning = True

        while self.keepRunning:
            self.result.emit(True)
            time.sleep(self.collect_slow_data_interval)

    def update(self, config):
        self.collect_slow_data_interval = config.getCollectSlowDataInterval()

    def stop(self):
        self.keepRunning = False

#Создаем воркер обновления иконки в трее
def startUpdateTrayIconWorker(self):
    self.update_tray_icon_worker = UpdateTrayIconWorker(self)
    self.update_tray_icon_worker.result.connect(self.updateTrayIcon)
    self.update_tray_icon_worker.start()

#Обработка данных из UpdateTrayIconWorker'а
def updateTrayIcon(self, result):
    data_lists = self.data_lists

    if len(data_lists['general_temps']) > 0:
        #Сформируем новое изображения трея
        self.image = support.getTrayImage(data_lists['current_temp'], self.config)

def updateWorkersCollectionInterval(self):
    self.collect_slow_worker.update(self.config)
    self.update_ui_scores_worker.update(self.config)
    self.update_tray_icon_worker.update(self.config)
    self.backup_worker.update(self.config)

def startWorkers(self):
    #Запустим воркеры для сбора данных
    startCollectSlowDataWorker(self)
    startCollectFastDataWorker(self)

    #Для обновления иконки трея
    startUpdateTrayIconWorker(self)

    #Для обновления GUI
    startUpdateUiScoresWorker(self)

    #Для бэкапа
    if self.config.getOpenMinimized:
        self.update_ui_scores_worker.stop()

    if self.config.getIsBackupNeeded():
        if support.getRestoredData(self):
            self.data_lists = support.getRestoredData(self)

        startBackupWorker(self)

    #И для мониторинга системных данных
    startSystemMonitoringWorker(self)

def stopWorkers(self):
    self.update_ui_scores_worker.stop()
    self.collect_fast_worker.stop()
    self.collect_slow_worker.stop()
    self.backup_worker.stop()
    self.system_monitoring_worker.stop()