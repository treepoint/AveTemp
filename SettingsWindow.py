from PyQt6 import QtWidgets
import windows.settingsWindow

import Entities

class Main(QtWidgets.QDialog,  windows.settingsWindow.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Дизайн

        self.buttonSaveSettings.clicked.connect(self.closeWindow)
        self.checkBoxCPUManagment.toggled.connect(self.enableCPUManagmentBlock)

        self.config = Entities.Config()

        self.labelNameAndVersion.setText(self.config.getName() + ' ' + self.config.getVersion())
        
    def setData(self, config):
        self.spinBoxLoggingInterval.setValue(config.collect_interval)
        self.checkBoxStoreStat.setChecked(config.is_backup_needed)
        self.checkBoxCloseToTray.setChecked(config.close_to_tray)
        self.checkBoxOpenMinimized.setChecked(config.open_minimized)
        self.checkBoxCPUManagment.setChecked(config.CPU_managment)
        self.spinBoxCPUTurboThreshhold.setValue(config.CPU_turbo_threshhold)
        self.spinBoxCPUTurboIdleState.setValue(config.CPU_turbo_idle_state)
        self.spinBoxCPUTurboLoadState.setValue(config.CPU_turbo_load_state)

    def enableCPUManagmentBlock(self):
        if self.checkBoxCPUManagment.isChecked():
            new_state = True
        else:
            new_state = False

        self.labelCPUThreshhold.setEnabled(new_state)
        self.spinBoxCPUTurboThreshhold.setEnabled(new_state)
        self.labelCPUTreshholdHint.setEnabled(new_state)

        self.labelCPUTurboIdleState.setEnabled(new_state)
        self.spinBoxCPUTurboIdleState.setEnabled(new_state)

        self.labelCPUTurboLoadState.setEnabled(new_state)
        self.spinBoxCPUTurboLoadState.setEnabled(new_state)
        self.labelCPUTurboLoadStateHint.setEnabled(new_state)

    def closeWindow(self):
        self.config.setCollectInterval(float(self.spinBoxLoggingInterval.value()))
        self.config.setIsBackupNeeded(self.checkBoxStoreStat.isChecked())
        self.config.setCloseToTray(self.checkBoxCloseToTray.isChecked())
        self.config.setOpenMinimized(self.checkBoxOpenMinimized.isChecked())
        
        self.config.setCPUManagment(self.checkBoxCPUManagment.isChecked())
        self.config.setCPUTurboThreshhold(int(self.spinBoxCPUTurboThreshhold.value()))
        self.config.setCPUTurboIdleState(int(self.spinBoxCPUTurboIdleState.value()))
        self.config.setCPUTurboLoadState(int(self.spinBoxCPUTurboLoadState.value()))

        self.accept()