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
        self.name = "AveTemp"
        self.version = "1.1.1"

    def get_collect_interval(self):
        return self.collect_interval

    def set_collect_interval(self, value):
        self.collect_interval = value

    def get_backup_interval(self):
        return self.backup_interval

    def get_store_period(self):
        return self.store_period

    def set_store_period(self, value):
        self.store_period = value

    def get_is_backup_needed(self):
        return self.is_backup_needed

    def set_is_backup_needed(self, value):
        self.is_backup_needed = value

    def get_close_to_tray(self):
        return self.close_to_tray

    def set_close_to_tray(self, value):
        self.close_to_tray = value

    def get_open_minimized(self):
        return self.open_minimized

    def set_open_minimized(self, value):
        self.open_minimized = value

    def get_name(self):
        return self.name

    def get_version(self):
        return self.version

class Status(enum.Enum):
    error = 1
    success = 2
    not_collect = 3