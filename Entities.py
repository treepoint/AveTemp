import enum

class Config:
    def __init__(self, 
                 collect_interval = 1, 
                 backup_interval = 15, 
                 is_backup_needed = True, 
                 store_period = 86400, 
                 close_to_tray = False, 
                 open_minimized = False,
                 is_CPU_managment_on = False,
                 CPU_threshhold = 20,
                 CPU_idle_state = 99,
                 CPU_load_state = 100,
                 is_turbo_managment_on = False,
                 CPU_turbo_idle_id = 0,
                 CPU_turbo_load_id = 2
                 ):
        #Общие
        self.collect_interval = collect_interval
        self.backup_interval = backup_interval
        self.is_backup_needed = is_backup_needed
        self.store_period = store_period
        self.close_to_tray = close_to_tray
        self.open_minimized = open_minimized
        self.current_language = 1
        #Управление процессором
        self.performance_CPU_mode_on = True
        self.CPU_idle_state_pause = 10
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
        self.autostart_is_active = False
        self.name = 'AveTemp'
        self.version = '1.3.2'

    #Локализация
    def getCurrentLanguage(self):
        return self.current_language

    def setCurrentLanguage(self, value):
        self.current_language = value

    #Общие
    def getCollectInterval(self):
        return self.collect_interval

    def setCollectInterval(self, value):
        self.collect_interval = value

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

    #Управление процессором
    def setPerformanceCPUModeOn(self, value):
        self.performance_CPU_mode_on = value

    def getPerformanceCPUModeOn(self):
        return self.performance_CPU_mode_on

    def getCPUIdleStatePause(self):
        return self.CPU_idle_state_pause

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

    def setAutostartIsActive(self, value):
        self.autostart_is_active = value

    def getAutostartIsActive(self):
        return self.autostart_is_active

    def getName(self):
        return self.name

    def getVersion(self):
        return self.version

class ConfigParser:
    def getMain(config):
        #Описание парсера
        return  {
                    #Общие
                    'collect_interval': config.collect_interval, 
                    'store_period' : config.store_period,
                    'is_backup_needed' : config.is_backup_needed,
                    'close_to_tray' : config.close_to_tray,
                    'open_minimized' : config.open_minimized,
                    #Управление процессором
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
        self.eco = {'id' : 0, 'name' : 'Минимальные частоты (энергоэффективно)', 'index': '000'}
        self.basic = {'id' : 1, 'name' : 'Базовые частоты (сбалансировано)', 'index': '004'}
        self.turbo = {'id' : 2, 'name' : 'Максимальные частоты (производительно)', 'index': '002'}

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