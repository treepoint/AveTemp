import enum

class Config:
    def __init__(self, 
                 collect_slow_data_interval = 1, 
                 collect_fast_data_interval = 0.1,
                 autostart_delay = 3,
                 backup_interval = 60, 
                 is_backup_needed = True, 
                 store_period = 86400, 
                 close_to_tray = False, 
                 open_minimized = False,
                 CPU_idle_state_pause = 50,
                 is_CPU_managment_on = False,
                 CPU_threshhold = 45,
                 CPU_idle_state = 60,
                 CPU_load_state = 100,
                 is_turbo_managment_on = False,
                 CPU_turbo_idle_id = 0,
                 CPU_turbo_load_id = 2
                 ):
        #Локализация
        self.current_language_code = 'en'
        
        #Общие
        self.collect_slow_data_interval = collect_slow_data_interval
        self.backup_interval = backup_interval
        self.is_backup_needed = is_backup_needed
        self.store_period = store_period
        self.close_to_tray = close_to_tray
        self.open_minimized = open_minimized

        #Автозагрузка
        self.autostart_is_active = False
        self.autostart_delay = autostart_delay

        #Управление процессором
        self.collect_fast_data_interval = collect_fast_data_interval
        self.performance_CPU_mode_on = True
        self.CPU_idle_state_pause = CPU_idle_state_pause
        self.is_CPU_managment_on = is_CPU_managment_on
        self.CPU_threshhold = CPU_threshhold
        self.CPU_idle_state = CPU_idle_state
        self.CPU_load_state = CPU_load_state

        #Управление турбо режимом
        self.is_turbo_managment_on = is_turbo_managment_on
        self.CPU_turbo_idle_id = CPU_turbo_idle_id
        self.CPU_turbo_load_id = CPU_turbo_load_id

        #Служебные
        self.system_uses_light_theme = False
        self.system_data_collect_interval = 300
        self.name = 'AveTemp'
        self.version = '1.4.1'

    #Локализация
    def getCurrentLanguageCode(self):
        return self.current_language_code

    def setCurrentLanguageCode(self, value):
        self.current_language_code = value

    #Общие
    def getCollectSlowDataInterval(self):
        return self.collect_slow_data_interval

    def setCollectSlowDataInterval(self, value):
        self.collect_slow_data_interval = value

    def getBackupInterval(self):
        return self.backup_interval

    def getStorePeriod(self):
        return self.store_period

    def setStorePeriod(self, value):
        self.store_period = value

    def getIsBackupNeeded(self):
        return self.is_backup_needed

    def setIsBackupNeeded(self, value):
        self.is_backup_needed = value

    def getCloseToTray(self):
        return self.close_to_tray

    def setCloseToTray(self, value):
        self.close_to_tray = value

    def getOpenMinimized(self):
        return self.open_minimized

    def setOpenMinimized(self, value):
        self.open_minimized = value

    #Автозагрузка
    def setAutostartIsActive(self, value):
        self.autostart_is_active = value

    def getAutostartIsActive(self):
        return self.autostart_is_active

    def setAutostartDelay(self, value):
        self.autostart_delay = value

    def getAutostartDelay(self):
        return self.autostart_delay

    #Управление процессором
    def getCollectFastDataInterval(self):
        return self.collect_fast_data_interval

    def setCollectFastDataInterval(self, value):
        self.collect_fast_data_interval = value

    def setPerformanceCPUModeOn(self, value):
        self.performance_CPU_mode_on = value

    def getPerformanceCPUModeOn(self):
        return self.performance_CPU_mode_on

    def getCPUIdleStatePause(self):
        return self.CPU_idle_state_pause

    def setCPUIdleStatePause(self, value):
        self.CPU_idle_state_pause = value

    def getIsCPUManagmentOn(self):
        return self.is_CPU_managment_on

    def setIsCPUManagmentOn(self, value):
        self.is_CPU_managment_on = value

    def getCPUThreshhold(self):
        return self.CPU_threshhold

    def setCPUThreshhold(self, value):
        self.CPU_threshhold = value

    def getCPUIdleState(self):
        return self.CPU_idle_state

    def setCPUIdleState(self, value):
        self.CPU_idle_state = value

    def getCPULoadState(self):
        return self.CPU_load_state
    
    def setCPULoadState(self, value):
        self.CPU_load_state = value
    
    #Управление турбо режимом
    def setIsTurboManagmentOn(self, value):
        self.is_turbo_managment_on = value

    def getIsTurboManagmentOn(self):
        return self.is_turbo_managment_on

    def setCPUTurboIdleId(self, value):
        self.CPU_turbo_idle_id = value

    def getCPUTurboIdleId(self):
        return self.CPU_turbo_idle_id

    def setCPUTurboLoadId(self, value):
        self.CPU_turbo_load_id = value

    def getCPUTurboLoadId(self):
        return self.CPU_turbo_load_id

    #Служебные
    def getSystemDataCollectIntreval(self):
        return self.system_data_collect_interval

    def setSystemUsesLightTheme(self, value):
        self.system_uses_light_theme = value

    def getSystemUsesLightTheme(self):
        return self.system_uses_light_theme

    def getName(self):
        return self.name

    def getVersion(self):
        return self.version

class ConfigParser:
    def getMain(config):
        #Описание парсера
        return  {
                    #Локализация
                    'current_language_code': config.current_language_code,
                    #Общие
                    'collect_slow_data_interval': config.collect_slow_data_interval, 
                    'store_period' : config.store_period,
                    'is_backup_needed' : config.is_backup_needed,
                    'close_to_tray' : config.close_to_tray,
                    'open_minimized' : config.open_minimized,
                    #Автозагрузка
                    'autostart_delay': config.autostart_delay,
                    #Управление процессором
                    'CPU_idle_state_pause' : config.CPU_idle_state_pause,
                    'collect_fast_data_interval' : config.collect_fast_data_interval,
                    'is_CPU_managment_on': config.is_CPU_managment_on,
                    'CPU_threshhold': config.CPU_threshhold,
                    'CPU_idle_state': config.CPU_idle_state,
                    'CPU_load_state': config.CPU_load_state,
                    #Управление турбо режимом
                    'is_turbo_managment_on': config.is_turbo_managment_on,
                    'CPU_turbo_idle_id': config.CPU_turbo_idle_id,
                    'CPU_turbo_load_id': config.CPU_turbo_load_id
                }

class Status(enum.Enum):
    error = 1
    success = 2
    not_collect = 3

class TurboStatuses:
    def __init__(self):
        self.eco = {'id' : 0, 'name' : 'min_freq', 'index': '000'}
        self.basic = {'id' : 1, 'name' : 'basic_freq', 'index': '004'}
        self.turbo = {'id' : 2, 'name' : 'max_freq', 'index': '002'}

    def getEco(self):
        return self.eco

    def getBasic(self):
        return self.basic

    def getTurbo(self):
        return self.turbo

    def getIndexById(self, id):
        if id == 0:
            return self.eco['index']
        elif id == 1:
            return self.basic['index']
        elif id == 2:
            return self.turbo['index']

class Languages:
    def __init__(self):
        self.en = {'code' : 'en', 'name': 'English'}
        self.ru = {'code' : 'ru', 'name': 'Русский'}

    def getEnglish(self):
        return self.en

    def getRussian(self):
        return self.ru

class Localizations:
    def getDictionary(self):
        dictionary = {
                            "en": {
                                "frequency": "Frequency",
                                "load": "Load",
                                "clear": "Clear",
                                "clear_all": "Clear all",
                                "averages": "Average values",
                                "minutes": "min",
                                "hour": "hour",
                                "24_hours": "24 hours",
                                "current_she": "Current",
                                "current_he": "Current",
                                "min": "Min",
                                "max": "Max",
                                "temp": "Temperature, C°",
                                "TDP": "Thermal Design Power, W",
                                "watt": "W",
                                "settings": "Settings",
                                "admin_rights": "Administrator rights are required for proper work",
                                "language": "Language: ",
                                "collection_interval_text": "Data collection interval, seconds: ",
                                "collect_and_restore_stat": "Store and retrieve statistics for a day",
                                "all_data_will_be_removed_when_off": "When disabled, all collected data will be deleted",
                                "close_to_tray": "Minimize to tray when closing",
                                "start_to_tray": "At startup minimize to system tray",
                                "autostart": "Autostart",
                                "add_to_autostart": "Run at startup",
                                "delay_before_start_sec_text": "Pause before startup, seconds:",
                                "autostart_delay_hint": "Delay to allow other programs to load without restriction",
                                "statistics": "Statistics",
                                "backup_interval_text": "Backup interval, minutes:",
                                "less_backup_interval_less_consumption_text": "The smaller the interval, the lower the consumption of resources in the background",
                                "cpu_modes_management": "Processor mode control",
                                "default_when_off": "When disabled, all settings return to defaults",
                                "auto_change_cpu_state": "Automatically change processor state",
                                "when_load_less_then_then": "When the load is below the threshold, the maximum state of the processor will be reduced to reduce the use of turbo mode at idle ",
                                "load_threshold": "Load threshold, all cores %:",
                                "idle_state": "Condition at idle, %:",
                                "load_state": "Condition under load, %:",
                                "state_less_than_100_will": "A value below 100% reduces the use of turbo boost in all scenarios",
                                "force_cpu_state": "Explicitly set the state of turbo mode",
                                "in_idle": "At idle:",
                                "on_load": "Under load:",
                                "min_freq": "Minimum frequencies (energy efficient)",
                                "basic_freq": "Base frequencies (balanced)",
                                "max_freq": "Maximum frequencies (productive)"
                                },
                            "ru": {
                                "frequency": "Частота",
                                "load": "Нагрузка",
                                "clear": "Очистить",
                                "clear_all": "Очистить все",
                                "averages": "Средние показатели",
                                "minutes": "мин",
                                "hour": "час",
                                "24_hours": "24 часа",
                                "current_she": "Текущая",
                                "current_he": "Текущий",
                                "min": "Мин",
                                "max": "Макс",
                                "temp": "Температура, С°",
                                "TDP": "Теплопакет, Вт",
                                "watt": "Вт",
                                "settings": "Настройки",
                                "admin_rights": "Для корректной работы нужны права администратора",
                                "language": "Язык: ",
                                "collection_interval_text": "Интервал сбора данных, секунды: ",
                                "collect_and_restore_stat": "Хранить и восстанавливать статистику за сутки",
                                "all_data_will_be_removed_when_off": "При отключении все собранные данные будут удалены",
                                "close_to_tray": "При закрытии сворачивать в трей",
                                "start_to_tray": "Запускать свернутым",
                                "autostart": "Автозагрузка",
                                "delay_before_start_sec_text": "Пауза перед запуском, секунды:",
                                "autostart_delay_hint": "Задержка, чтобы дать другим программам загрузится без ограничений",
                                "add_to_autostart": "Добавить в автозагрузку",
                                "statistics": "Статистика",
                                "backup_interval_text": "Интервал сохранения, минуты:",
                                "less_backup_interval_less_consumption_text": "Чем меньше интервал, тем меньше фоновое потребление ресурсов",
                                "cpu_modes_management": "Управление режимами работы процессора",
                                "default_when_off": "При отключении все настройки возвращаются к стандартным",
                                "auto_change_cpu_state": "Автоматически изменять состояние процессора",
                                "when_load_less_then_then": "При нагрузке ниже порога, максимальное состояние процессора будет ограничено, чтобы снизить использование турбо режима в простое ",
                                "load_threshold": "Порог нагрузки, все ядра %:",
                                "idle_state": "Состояние в простое, %:",
                                "load_state": "Состояние под нагрузкой, %:",
                                "state_less_than_100_will": "Значение ниже 100% снижает использование турбо буста в любых сценариях",
                                "force_cpu_state": "Явно задавать состояние турбо режима",                            
                                "in_idle": "В простое:",
                                "on_load": "Под нагрузкой:",
                                "min_freq": "Минимальные частоты (энергоэффективно)",
                                "basic_freq": "Базовые частоты (сбалансировано)",
                                "max_freq": "Максимальные частоты (производительно)"                        
                                }
                            }

        return dictionary