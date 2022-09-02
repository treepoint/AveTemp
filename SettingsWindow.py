from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

import Entities

class Main(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('windows/settings.ui', self)

        self.buttonSaveSettings.clicked.connect(self.closeWindow)

        self.config = Entities.Config()

        self.labelNameAndVersion.setText(self.config.get_name() + ' ' + self.config.get_version())
        
    def setData(self, config):
        self.spinBoxLoggingInterval.setValue(config.collect_interval)
        self.checkBoxCloseToTray.setChecked(config.close_to_tray)
        self.checkBoxOpenMinimized.setChecked(config.open_minimized)

    def closeWindow(self):
        self.config.set_collect_interval(float(self.spinBoxLoggingInterval.value()))
        self.config.set_close_to_tray(self.checkBoxCloseToTray.isChecked())
        self.config.set_open_minimized(self.checkBoxOpenMinimized.isChecked())

        self.accept()