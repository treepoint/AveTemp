import enum

class Config:
    def __init__(self, 
                 collect_interval=1, 
                 backup_interval = 15, 
                 is_backup_needed = True, 
                 store_period=86400, 
                 close_to_tray=False, 
                 open_minimized=False):
        self.collect_interval = collect_interval
        self.backup_interval = backup_interval
        self.is_backup_needed = is_backup_needed
        self.store_period = store_period
        self.close_to_tray = close_to_tray
        self.open_minimized = open_minimized
        self.systemUsesLightTheme = False
        self.name = "AveTemp"
        self.version = "1.2.0"

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

    def setSystemUsesLightTheme(self, value):
        self.systemUsesLightTheme = value

    def getSystemUsesLightTheme(self):
        return self.systemUsesLightTheme

    def getName(self):
        return self.name

    def getVersion(self):
        return self.version

class Status(enum.Enum):
    error = 1
    success = 2
    not_collect = 3