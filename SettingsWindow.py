from PyQt6 import QtWidgets
import windows.settingsWindow

import Entities
import support
import localization
loader = localization.Loader()

from pyi18n import PyI18n

class Main(QtWidgets.QDialog,  windows.settingsWindow.Ui_Dialog):
    def __init__(self, locale, parent=None):
        super().__init__(parent)
        self.setupUi(self, locale)  # Дизайн

        self.config = Entities.Config()

        self.buttonSaveSettings.clicked.connect(self.closeWindow)
        self.checkBoxCPUManagment.toggled.connect(self.enableCPUManagmentBlock)

        self.labelNameAndVersion.setText(self.config.getName() + ' ' + self.config.getVersion())
        
    def setData(self, config, turbo_statuses):
        #Селект локализации
        #TODO: в конфиг

        #self.comboBoxLanguage.addItem('Русский', 'ru')
        #self.comboBoxLanguage.addItem('English', 'en')

        #Базовые настройки
        self.spinBoxLoggingInterval.setValue(config.getCollectInterval())
        self.checkBoxStoreStat.setChecked(config.getIsBackupNeeded())
        self.checkBoxCloseToTray.setChecked(config.getCloseToTray())
        self.checkBoxOpenMinimized.setChecked(config.getOpenMinimized())
        self.checkBoxAutostartIsActive.setChecked(config.getAutostartIsActive())

        #Управление процессором
        self.checkBoxCPUManagment.setChecked(config.getIsCPUManagmentOn())
        self.spinBoxCPUThreshhold.setValue(config.getCPUThreshhold())
        self.spinBoxCPUIdleState.setValue(config.getCPUIdleState())
        self.spinBoxCPULoadState.setValue(config.getCPULoadState())

        #Инициализируем выпадающие селекты турбо    
        #TODO: do better way and fix the locale for auto-py-to-exec
        i18n = PyI18n(("en", "ru"), loader=loader)

        trans = i18n.gettext

        locale = support.getCurrentSystemLanguage()

        self.comboBoxCPUTurboIdleState.addItem(trans(locale, turbo_statuses.getEco()['name']), turbo_statuses.getEco()['id'])
        self.comboBoxCPUTurboIdleState.addItem(trans(locale, turbo_statuses.getBasic()['name']), turbo_statuses.getBasic()['id'])

        self.comboBoxCPUTurboLoadState.addItem(trans(locale, turbo_statuses.getBasic()['name']), turbo_statuses.getBasic()['id'])
        self.comboBoxCPUTurboLoadState.addItem(trans(locale, turbo_statuses.getTurbo()['name']), turbo_statuses.getTurbo()['id'])

        #Управление турбо режимом
        self.checkBoxCPUTurboManagment.setChecked(config.getIsTurboManagmentOn())

        idleComboboxIndex = self.comboBoxCPUTurboIdleState.findData(config.getCPUTurboIdleId())
        loadComboboxIndex = self.comboBoxCPUTurboLoadState.findData(config.getCPUTurboLoadId())

        self.comboBoxCPUTurboIdleState.setCurrentIndex(idleComboboxIndex)
        self.comboBoxCPUTurboLoadState.setCurrentIndex(loadComboboxIndex)

    def enableCPUManagmentBlock(self):
        if self.checkBoxCPUManagment.isChecked():
            new_state = True
        else:
            new_state = False

        self.labelCPUThreshhold.setEnabled(new_state)
        self.spinBoxCPUThreshhold.setEnabled(new_state)
        self.labelCPUTreshholdHint.setEnabled(new_state)

        self.labelCPUIdleState.setEnabled(new_state)
        self.spinBoxCPUIdleState.setEnabled(new_state)

        self.labelCPULoadState.setEnabled(new_state)
        self.spinBoxCPULoadState.setEnabled(new_state)
        self.labelCPULoadStateHint.setEnabled(new_state)

        self.checkBoxCPUTurboManagment.setEnabled(new_state)
        self.labelCPUTurboManagment.setEnabled(new_state)
        self.labelCPUTurboIdleState.setEnabled(new_state)
        self.comboBoxCPUTurboIdleState.setEnabled(new_state)
        self.labelCPUTurboLoadState.setEnabled(new_state)
        self.comboBoxCPUTurboLoadState.setEnabled(new_state)

    def closeWindow(self):
        #Локализация
        #TODO: get back
        #self.config.setCurrentLanguage(self.comboBoxLanguage.currentData())

        #Базовые настройки
        self.config.setCollectInterval(float(self.spinBoxLoggingInterval.value()))
        self.config.setIsBackupNeeded(self.checkBoxStoreStat.isChecked())
        self.config.setCloseToTray(self.checkBoxCloseToTray.isChecked())
        self.config.setOpenMinimized(self.checkBoxOpenMinimized.isChecked())
        self.config.setAutostartIsActive(self.checkBoxAutostartIsActive.isChecked())
        
        #Управление процессором
        self.config.setIsCPUManagmentOn(self.checkBoxCPUManagment.isChecked())
        self.config.setCPUThreshhold(int(self.spinBoxCPUThreshhold.value()))
        self.config.setCPUIdleState(int(self.spinBoxCPUIdleState.value()))
        self.config.setCPULoadState(int(self.spinBoxCPULoadState.value()))

        #Управление турбо режимом
        self.config.setIsTurboManagmentOn(self.checkBoxCPUTurboManagment.isChecked())
        self.config.setCPUTurboIdleId(self.comboBoxCPUTurboIdleState.currentData())
        self.config.setCPUTurboLoadId(self.comboBoxCPUTurboLoadState.currentData())

        self.accept()