from math import inf
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem

import SettingsWindow
import windows.mainWindow

import hardware
import Entities
import support
import workers
import taskManager
import localization

trans = localization.trans
languages = Entities.Languages()

class Main(QMainWindow,  windows.mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Прочитаем конфиг
        self.config = Entities.Config()
        support.readConfig(self)

        #Дизайн
        self.setupUi(self, self.config.getCurrentLanguageCode()) 

        #Включаем мониторинг и объект, откуда брать данные
        self.computer = hardware.initHardware()

        #Листы для хранения данных
        self.data_lists = {
                            'general_temps' : [], 
                            'average_temps' : [],
                            'general_TDP' : [],
                            'average_TDP' : [],
                            'all_load' : [],
                            'current_temp' : 0,
                            'min_temp' : 0,
                            'max_temp' : 0,
                            'current_TDP' : 0,
                            'min_TDP' : 0,
                            'max_TDP' : 0,
                            'cpu' : 
                                    { 
                                        'cores' : [],
                                        'threads' : [],
                                    }
                         }

        if self.config.getIsBackupNeeded():
            if support.getRestoredData(self):
                self.data_lists = support.getRestoredData(self)

            self.startBackupWorker()

        self.startSystemMonitoringWorker()

        if self.config.getIsCPUManagmentOn():
            CPU_performance_mode = hardware.setCpuPerformanceState(self.config, self.data_lists)
            self.config.setPerformanceCPUModeOn(CPU_performance_mode)
        
        cores_and_threads = hardware.getCoresAndThreadsCount(self.computer)

        self.cpu_cores = cores_and_threads['cores_count']
        self.cpu_threads = cores_and_threads['threads_count']

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
        self.collect_slow_data_interval = self.config.getCollectSlowDataInterval()

        #А это коэффициент, зависящий от сбора, чтобы вне зависимости от частоты сбора, 
        #мы всегда брали столько показаний, сколько нужно для временных рамок.
        #Условно, нам надо брать за минуту, то частота сбора 0.5, тогда из листов мы будем брать не 60 показаний
        #А 60*2, где 2 — self.collect_slow_data_interval
        self.collect_koef = round(1/self.collect_slow_data_interval)

        #Проставим название проца
        self.setCpuName()

        #Зададим размеры окошка исходя из оборудования
        self.setWindowsSizes()

        #Обработка кнопок
        self.buttonResetGeneralTemps.clicked.connect(self.resetGeneralTemps)
        self.buttonResetTDP.clicked.connect(self.resetTDP)
        self.buttonResetAverageTemps.clicked.connect(self.resetAverage)
        self.buttonShowSettings.clicked.connect(self.showSettings)

        #Запустим воркеры для сбора данных
        self.startCollectSlowDataWorker()
        self.startCollectFastDataWorker()

        #И для обновления интерфейса
        self.startUpdateUiScoresWorker()

        #Плашка если нет админских прав
        if support.isThereAdminRight():
            self.frameAdminRight.setVisible(False)

    #Перезаписываем событие не закрытие, чтобы скрывать в трей если это надо
    def closeEvent(self, event):
        if self.config.getCloseToTray():
            event.ignore()
            self.hide()
        else:
            #Иначе стопнем воркеры
            self.collect_fast_worker.stop()
            self.collect_slow_worker.stop()
            self.update_ui_scores_worker.stop()
            self.backup_worker.stop()

            #вернем лимиты проца по умолчанию — 100
            hardware.setCPUStatetoDefault()
            hardware.setTurboToDefault()

            #Закроем мониторинг оборудования
            hardware.closeHardware(self.computer)

    def startCollectSlowDataWorker(self):
        #Создаем воркер для сбора и обновления информации
        self.collect_slow_worker = workers.CollectSlowDataWorker(self)
        self.collect_slow_worker.result.connect(self.processSlowData)
        self.collect_slow_worker.start()

    def startCollectFastDataWorker(self):
        #Создаем воркер для мониторинга нагрузки на CPU
        self.collect_fast_worker = workers.CollectFastDataWorker(self)
        self.collect_fast_worker.result.connect(self.processFastData)
        self.collect_fast_worker.start()

    def startBackupWorker(self):
        #Создаем воркер для бэкапа данных
        self.backup_worker = workers.BackupWorker(self)
        self.backup_worker.result.connect(self.saveData)
        self.backup_worker.start()

    def startSystemMonitoringWorker(self):
        #Создаем воркер для мониторинга системных параметров
        self.system_monitoring_worker = workers.SystemMonitoringWorker(self)
        self.system_monitoring_worker.result.connect(self.updateSystemStateConfig)
        self.system_monitoring_worker.start()

    def startUpdateUiScoresWorker(self):
        #Создаем воркер обновления показателей интерфейса.
        #У нас теперь данные стекаются с разных воркеров, так что обновлять надо централизовано
        self.update_ui_scores_worker = workers.UpdateUiScoresWorker(self)
        self.update_ui_scores_worker.result.connect(self.updateUiScores)
        self.update_ui_scores_worker.start()

    #Функции для сбора записанных данных
    def resetGeneralTemps(self):
        self.data_lists['general_temps'] = []
        self.data_lists['current_temp'] = 0
        self.data_lists['min_temp'] = 0
        self.data_lists['max_temp'] = 0

    def resetTDP(self):
        self.data_lists['general_TDP'] = []
        self.data_lists['current_TDP'] = 0
        self.data_lists['min_TDP'] = 0
        self.data_lists['max_TDP'] = 0

    def resetAverage(self):
        self.data_lists['average_temps'] = []
        self.data_lists['average_TDP'] = []

    def resetAllData(self):
        self.resetGeneralTemps()
        self.resetTDP()
        self.resetAverage()

    def setCpuName(self):
        cpu_name = hardware.getCpuName(self.computer)
        cpu_name_with_counts = f"{ cpu_name } ({ str(self.cpu_cores) }/{ str(self.cpu_threads) })"
        self.cpuNameLabel.setText(cpu_name_with_counts)

    def setWindowsSizes(self):
        additional_cpu_cores_height = (self.cpu_cores - 6) * 24

        self.resize(400, 330 + additional_cpu_cores_height)

    def getAvgTempForSeconds(self, collect_slow_data_interval):
        average_temps_sum_perion = sum(self.data_lists['average_temps'][:collect_slow_data_interval*self.collect_koef])
        average_temps_len_perion = len(self.data_lists['average_temps'][:collect_slow_data_interval*self.collect_koef])

        return average_temps_sum_perion/average_temps_len_perion

    def getAvgTDPForSeconds(self, collect_slow_data_interval):
        average_TDPs_sum_perion = sum(self.data_lists['average_TDP'][:collect_slow_data_interval*self.collect_koef])
        average_TDPs_len_perion = len(self.data_lists['average_TDP'][:collect_slow_data_interval*self.collect_koef])

        return average_TDPs_sum_perion/average_TDPs_len_perion

    #Записываем данные по температуре
    def writeTempData(self, result):        
        #Записываем значения
        cpu_temp = round(result['cpu']['temp'], 1)

        if cpu_temp > 0:
            self.data_lists['general_temps'].insert(0, result['cpu']['temp'])
            self.data_lists['average_temps'].insert(0, result['cpu']['temp'])

            if cpu_temp < self.data_lists['min_temp'] or self.data_lists['min_temp'] == 0:
                self.data_lists['min_temp'] = cpu_temp

            if cpu_temp > self.data_lists['max_temp']:
                self.data_lists['max_temp'] = cpu_temp

            self.data_lists['current_temp'] = cpu_temp
        
        #Обрезаем массивы
        self.data_lists['general_temps'] = self.data_lists['general_temps'][:self.store_period]
        self.data_lists['average_temps'] = self.data_lists['average_temps'][:self.store_period]

    #Записываем данные по TDP
    def writeTDPData(self, result):         
        cpu_TDP = round(result['cpu']['tdp'], 1)

        if cpu_TDP > 0 and cpu_TDP != inf:
            self.data_lists['general_TDP'].insert(0, result['cpu']['tdp'])
            self.data_lists['average_TDP'].insert(0, result['cpu']['tdp'])

            if (cpu_TDP < self.data_lists['min_TDP']) or self.data_lists['min_TDP'] == 0:
                self.data_lists['min_TDP'] = cpu_TDP

            if cpu_TDP > self.data_lists['max_TDP']:
                self.data_lists['max_TDP'] = cpu_TDP

            self.data_lists['current_TDP'] = cpu_TDP

        #Обрезаем массив
        self.data_lists['general_TDP'] = self.data_lists['general_TDP'][:self.store_period]
        self.data_lists['average_TDP'] = self.data_lists['average_TDP'][:self.store_period]

    #Записываем данные по ядрам
    def writeCoresData(self, result):  
        cores = []   
        for core in result['cpu']['cores']:
            cores.append({'id': int(core['id'])-1, 'clock' : str(core['clock'])})

        self.data_lists['cpu']['cores'] = cores

    #Записываем данные по потокам
    def writeThreadsData(self, result):
        threads = []

        for thread in result['cpu']['threads']:
            load = support.toRoundStr(thread['load'])
            threads.append({'id': int(thread['id'])-1, 'load' : load})

        self.data_lists['cpu']['threads'] = threads

        if round(result['all_load'], 1) > 0 and result['all_load'] != inf:
            self.data_lists['all_load'].insert(0, result['all_load'])

        self.data_lists['all_load'] = self.data_lists['all_load'][:self.store_period]

    #Обработка данных из collectWorker'а
    def processSlowData(self, result):        
        self.writeTempData(result)
        self.writeTDPData(result)
        self.writeCoresData(result)

    #Обработка данных из CpuLoadMonitoringWorker'а
    def processFastData(self, result):
        if not self.config.getIsCPUManagmentOn():
            CPU_performance_mode = False
        else:
            CPU_performance_mode = hardware.setCpuPerformanceState(self.config, self.data_lists)

        self.config.setPerformanceCPUModeOn(CPU_performance_mode)

        self.writeThreadsData(result)

    #Обновляем показатели в интерфейсе
    def updateUiScores(self, result):

        locale = self.config.getCurrentLanguageCode()
        
        if len(self.data_lists['general_temps']) > 0:
            #Сформируем новое изображения трея
            self.image = support.getTrayImage(self.data_lists['current_temp'], self.config)

            #Минимальная
            self.lineEditCpuMinTemp.setText(str(self.data_lists['min_temp']))
            #Текущая
            self.lineEditCpuCurrentTemp.setText(str(self.data_lists['current_temp']))
            #Максимальная
            self.lineEditCpuMaxTemp.setText(str(self.data_lists['max_temp']))

        if len(self.data_lists['general_TDP']) > 0:
            #Минимальный
            self.lineEditCpuMinTDP.setText(str(self.data_lists['min_TDP']))
            #Текущий
            self.lineEditCpuCurrentTDP.setText(str(self.data_lists['current_TDP']))
            #Максимальный
            self.lineEditCpuMaxTDP.setText(str(self.data_lists['max_TDP']))

        if len(self.data_lists['average_temps']) > 0:

            row = 0

            for minutes in (1, 5, 15, 60, 60*24):
                avg_temp = support.toRoundStr(self.getAvgTempForSeconds(60*minutes))
                avg_tdp = support.toRoundStr(self.getAvgTDPForSeconds(60*minutes))

                self.tableAverage.setItem(row, 0, QTableWidgetItem(f"{ avg_temp } С°"))            
                self.tableAverage.setItem(row, 1, QTableWidgetItem(f"{ avg_tdp } { trans(locale, 'watt') }"))

                row += 1

        for core in self.data_lists['cpu']['cores']:
            self.CPUinfoTable.setItem(core['id'], 0, QTableWidgetItem(core['clock']))

        #Идем по физическим ядрам, потому что нам надо сопоставить нагрузку между потоками и ядрами   
        for index, thread in enumerate(self.data_lists['cpu']['threads']):
            if self.SMT:
                load = support.toRoundStr((
                                            float(self.data_lists['cpu']['threads'][(thread['id']-1)*2]['load']) + 
                                            float(self.data_lists['cpu']['threads'][(thread['id']-1)*2-1]['load'])
                                            )/2)
            else:
                load = str(thread['load'])

            self.CPUinfoTable.setItem(thread['id'], 1, QTableWidgetItem(f"{ load }%"))

            if self.SMT and index + 1 == (self.cpu_threads/2):
                break

    #Обработка данных из backupWorker'а
    def saveData(self):
        support.saveData(self)

    #Обработка данных из SystemMonitoringWorker'а
    def updateSystemStateConfig(self, data):
        self.config.setSystemUsesLightTheme(data['system_uses_light_theme'])

        support.writeToConfig(self.config)
        new_config = support.readConfig(self)

        self.collect_slow_worker.update(new_config)

    def showSettings(self):
        locale = self.config.getCurrentLanguageCode()

        window = SettingsWindow.Main(locale)
                
        app_icon = support.getResourcePath('./images/icon.png')

        window.setWindowIcon(QIcon(app_icon))

        window.setData(self.config)

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

            #Управление автостартом
            if window.config.getAutostartIsActive():
                if not self.config.getAutostartIsActive():
                    taskManager.addToAutostart(self)

            else:
                if self.config.getAutostartIsActive():
                    taskManager.removeFromAutostart(self)

            #Обновим локализацию если надо
            if window.config.getCurrentLanguageCode() != self.config.getCurrentLanguageCode():
                self.retranslateUi(window, window.config.getCurrentLanguageCode())

            #Обновим конфиг и перечитаем его
            support.writeToConfig(window.config)
            new_config = support.readConfig(self)

            #Обновим время обновления данных
            self.collect_slow_worker.update(new_config)
            self.update_ui_scores_worker.update(new_config)

            window.destroy()