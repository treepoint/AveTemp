from PyQt6 import QtWidgets
import windows.settingsWindow

import Entities

class Main(QtWidgets.QDialog,  windows.settingsWindow.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Дизайн

        self.buttonSaveSettings.clicked.connect(self.closeWindow)

        self.config = Entities.Config()

        self.labelNameAndVersion.setText(self.config.getName() + ' ' + self.config.getVersion())
        
    def setData(self, config):
        self.spinBoxLoggingInterval.setValue(config.collect_interval)
        self.checkBoxStoreStat.setChecked(config.is_backup_needed)
        self.checkBoxCloseToTray.setChecked(config.close_to_tray)
        self.checkBoxOpenMinimized.setChecked(config.open_minimized)

    def closeWindow(self):
        self.config.setCollectInterval(float(self.spinBoxLoggingInterval.value()))
        self.config.setIsBackupNeeded(self.checkBoxStoreStat.isChecked())
        self.config.setCloseToTray(self.checkBoxCloseToTray.isChecked())
        self.config.setOpenMinimized(self.checkBoxOpenMinimized.isChecked())

        self.accept()