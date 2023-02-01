from PyQt6.QtCore import QThread, pyqtSignal

import time
import registry
import hardware
import system

# Воркер для обновления информации в трее
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

# Воркер для сбора данных
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
        self.config = config

    def stop(self):
        self.keepRunning = False

# Воркер для мониторинга нагрузки на CPU
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
            data = hardware.collectFastData(self.computer, self.data_lists, self.cpu_cores, self.cpu_threads)
            self.result.emit(data)
            time.sleep(self.collect_fast_data_interval)

    def update(self, config):
        self.collect_fast_data_interval = config.getCollectFastDataInterval()
        self.config = config

    def stop(self):
        self.keepRunning = False

# Воркер для бэкапа данных
class BackupWorker(QThread):
    def __init__(self, app_self):
        super().__init__()

        self.backup_interval = app_self.config.getBackupInterval()

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

# Воркер для обновления показателей в интерфейсе
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
        self.config = config

    def stop(self):
        self.keepRunning = False

# Воркер для обновления изображения в трее
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
        self.config = config

    def stop(self):
        self.keepRunning = False