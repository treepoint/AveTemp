from PyQt6.QtCore import QThread, pyqtSignal

import time
import registry
import hardware

class AppWorker(QThread):
    def __init__(self, app, collect_interval):
        super().__init__()

        self.collect_interval = collect_interval
        self.app = app

    result = pyqtSignal(bool)

    def run(self):
        self.keepRunning = True
        while self.keepRunning:
            time.sleep(self.collect_interval)

            if self.app.lastWindowClosed:
                self.result.emit(True)
            else:
                self.result.emit(False)

    def stop(self):
        self.keepRunning = False

# Воркер для сбора данных
class CollectWorker(QThread):
    def __init__(self, config, data_lists, cpu_cores, cpu_threads):
        super().__init__()

        self.collect_interval = config.getCollectInterval()
        self.config = config
        self.data_lists = data_lists
        self.cpu_cores = cpu_cores
        self.cpu_threads = cpu_threads

    result = pyqtSignal(dict, bool)

    def run(self):
        self.keepRunning = True
        while self.keepRunning:
            data = hardware.collectData(self.data_lists, self.cpu_cores, self.cpu_threads)

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