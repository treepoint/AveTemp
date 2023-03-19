from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow
import copy

import SettingsWindow
import windows.mainWindow

import hardware
import Entities
import support
import workers
import taskManager
import system
import data
import update
import alerts
import processes
import logger

app_icon = support.getResourcePath('./images/icon.png')
data_lists = Entities.DataLists()

class Main(QMainWindow,  windows.mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main()
    
    @logger.log
    def main(self):
        logger.setDebug(self)

        self.config = Entities.Config()
        support.readConfig(self)

        #Если уже запущен — выходим
        if processes.alreadyRunning(self):
            raise Exception('AveTemp is already running')
        
        system.increase_current_process_priority(self)

        #Применим текущие настройки процессора
        if self.config.getIsCPUManagmentOn():
            hardware.updateCPUParameters(self, self.config)

        #Листы для хранения данных
        self.data_lists = data_lists.get()

        #Включаем мониторинг и объект, откуда брать данные
        self.computer = hardware.initHardware(self)

        #Данные по ядрам и потокам
        cores_and_threads = hardware.getCoresAndThreadsCount(self)
        self.cpu_cores = cores_and_threads['cores_count']
        self.cpu_threads = cores_and_threads['threads_count']

        #Есть ли HT/SMT
        self.SMT = hardware.checkSMT(self)

        #Проставляем режим работы процесора
        if self.config.getIsCPUManagmentOn():
            CPU_performance_mode = hardware.setCpuPerformanceState(self)
            self.config.setIsCPUinLoadMode(CPU_performance_mode)
         
        #За сколько секунд храним данные, 86400 — сутки
        self.store_period = self.config.getStorePeriod()

        #Интервал сбора
        self.collect_slow_data_interval = self.config.getCollectSlowDataInterval()

        #Коэффицент чтобы вне зависимости от частоты сбора, мы всегда брали столько показаний, 
        #сколько нужно для временных рамок. Условно, нам надо брать за минуту, то частота сбора 0.5, 
        # тогда из листов мы будем брать не 60 показаний, а 60*2, где 2 — self.collect_slow_data_interval
        self.collect_koef = round(1/self.collect_slow_data_interval)

        #Инициализируем текстовки для перевода, чтобы можно было их обновлять
        self.locale = self.config.getCurrentLanguageCode()
        self.localizations = Entities.Localizations()

        #Обновим название программы и версию в интерфейсе
        support.updateNameAndVersion(self)

        #Интерфейс
        self.setupUi(self, self.locale) 
        
        #Проставим размер таблицы для проца
        self.CPUinfoTable.setRowCount(self.cpu_cores)

        #Обработка кнопок
        self.setupButtonsActions()

        #Проставим для трея картинку-заглушку
        self.image = support.getTrayImage(0, self.config)

        #Проставим название проца
        self.setCpuName()
        
        workers.startWorkers(self)

        self.is_alert_showing = False
        self.is_alert_expand = False

        support.checkAdminRights(self)
        update.checkUpdates(self)

        support.setComponentsSize(self)

    @logger.log
    def setupButtonsActions(self):
        self.buttonResetGeneralTemps.pressed.connect(self.resetGeneralTemps)
        self.buttonResetTDP.pressed.connect(self.resetTDP)
        self.buttonResetAverageTemps.pressed.connect(self.resetAverage)
        self.buttonShowSettings.pressed.connect(self.showSettings)
        self.buttonAlertExpand.pressed.connect(self.expandAlert)
        self.buttonAlertClose.pressed.connect(self.closeAlert)

    def resetGeneralTemps(self):
        data.resetGeneralTemps(self)

    def resetTDP(self):
        data.resetTDP(self)

    def resetAverage(self):
        data.resetAverage(self)

    def closeAlert(self):
        alerts.closeAlert(self)

    def expandAlert(self):
        alerts.expandAlert(self)

    def processSlowData(self, result):
        workers.processSlowData(self, result)

    def processFastData(self, result):
        workers.processFastData(self, result)

    def saveStatistics(self, result):
        workers.saveStatistics(self)

    def updateSystemStateConfig(self, result):
        workers.updateSystemStateConfig(self, result)

    def updateUiScores(self, result):
        workers.updateUiScores(self)

    def updateTrayIcon(self, result):
        workers.updateTrayIcon(self)

    @logger.log
    def showEvent(self, event):
        #Как появилось окно — запустим воркер обновления интерфейса
        self.update_ui_scores_worker.start()

    #Перезаписываем событие не закрытие, чтобы скрывать в трей если это надо
    @logger.log
    def closeEvent(self, event):
        if self.config.getCloseToTray():
            event.ignore()
            self.hide()
            self.update_ui_scores_worker.stop()
        else:
            workers.stopWorkers(self)
            hardware.setCPUtoDefault(self)
            #Выключим мониторинг оборудования
            hardware.closeHardware(self)

    @logger.log
    def setCpuName(self):
        cpu_name = hardware.getCpuName(self)
        cpu_name_with_counts = f"{ cpu_name } ({ str(self.cpu_cores) }/{ str(self.cpu_threads) })"
        self.cpuNameLabel.setText(cpu_name_with_counts)

    @logger.log
    def showSettings(self):

        window = SettingsWindow.Main(self.locale)
        window.setWindowIcon(QIcon(app_icon))
        window.setData(self.config)

        if window.exec():
            #Временно запишем старый конфиг, чтобы было что с чем сравнивать
            current_config = copy.copy(self.config)

            #Обновим и перечитаем новый конфиг
            support.writeToConfig(window.config)
            self.config = support.readConfig(self)

            #Проставим параметры, которые по умолчанию читаем не из сохраненного конфига
            self.config.setAutostartIsActive(window.config.getAutostartIsActive())

            if current_config.getIsBackupNeeded() and not self.config.getIsBackupNeeded():
                self.backup_worker.stop()
                support.removeStatFile()
            
            if not current_config.getIsBackupNeeded() and self.config.getIsBackupNeeded():
                workers.startBackupWorker(self)
                support.saveStatistics(self)
            
            #И если пользователь отключил управление процом — выставим все в сотку и турбо без ограничений, обычно это дефолт
            if self.config.getIsCPUManagmentOn() == False and (self.config.getIsCPUManagmentOn() != current_config.getIsCPUManagmentOn()):
                hardware.setCPUtoDefault(self)
            
            #Иначе позаботимся обновить ограничения процессора если они поменялись
            else:
                hardware.updateCPUParameters(self, current_config)

            #Обновим локализацию если надо
            new_locale = window.config.getCurrentLanguageCode()
            if self.locale != new_locale:
                self.retranslateUi(window, new_locale)
                self.locale = new_locale

            #Управление автостартом
            if self.config.getAutostartIsActive():
                if not current_config.getAutostartIsActive():
                    #Добавим, если только включили
                    taskManager.addToAutostart(self)
                elif int(self.config.getAutostartDelay()) != int(current_config.getAutostartDelay()):
                    #Обновим, если изменили значение паузы
                    taskManager.addToAutostart(self)

            else:
                if current_config.getAutostartIsActive():
                    taskManager.removeFromAutostart(self)

            #Обновим время обновления данных
            workers.updateWorkersCollectionInterval(self)

            window.destroy()