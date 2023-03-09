from PyQt6 import QtWidgets

import windows.settingsWindow
import logger

import Entities
languages = Entities.Languages()

class Main(QtWidgets.QDialog,  windows.settingsWindow.Ui_Dialog):
    def __init__(self, locale, parent=None):
        super().__init__(parent)

        logger.setDebug(self)
        self.main(locale)

    @logger.log
    def main(self, locale):

        self.config = Entities.Config()

        self.setupUi(self, locale)

        self.buttonSaveSettings.pressed.connect(self.closeWindow)
        self.checkBoxCPUManagment.toggled.connect(self.switchCPUManagmentBlock)
        self.checkBoxAutostartIsActive.toggled.connect(self.switchAutostartBlock)
        self.checkBoxStoreStat.toggled.connect(self.switchStatisticsBlock)

    @logger.log
    def reloadUi(self, index):
        self.retranslateUi(self, self.comboBoxLanguage.currentData())

    @logger.log
    def setData(self, config):
        #Селект локализации
        self.comboBoxLanguage.addItem(languages.getRussian()['name'], languages.getRussian()['code'])
        self.comboBoxLanguage.addItem(languages.getEnglish()['name'], languages.getEnglish()['code'])
        #Зададим выбранный сейчас
        currentLanguageIndex = self.comboBoxLanguage.findData(config.getCurrentLanguageCode())

        self.comboBoxLanguage.setCurrentIndex(currentLanguageIndex)

        #Повесим на смену чекбокса перевод UI
        self.comboBoxLanguage.currentIndexChanged.connect(self.reloadUi)

        #Базовые настройки
        self.spinBoxLoggingInterval.setValue(config.getCollectSlowDataInterval())
        self.checkBoxCloseToTray.setChecked(config.getCloseToTray())
        self.checkBoxOpenMinimized.setChecked(config.getOpenMinimized())

        #Автозагрузка
        self.checkBoxAutostartIsActive.setChecked(config.getAutostartIsActive())
        self.spinBoxAutostartDelay.setValue(config.getAutostartDelay())

        #Статистика
        self.checkBoxStoreStat.setChecked(config.getIsBackupNeeded())
        self.spinBoxBackupInterval.setValue(config.getBackupInterval())

        #Управление процессором
        self.checkBoxCPUManagment.setChecked(config.getIsCPUManagmentOn())
        self.spinBoxCPUThreshhold.setValue(config.getCPUThreshhold())
        self.spinBoxCPUIdleState.setValue(config.getCPUIdleState())
        self.spinBoxCPULoadState.setValue(config.getCPULoadState())

        #Управление турбо режимом
        self.checkBoxCPUTurboManagment.setChecked(config.getIsTurboManagmentOn())

        idleComboboxIndex = self.comboBoxCPUTurboIdleState.findData(config.getCPUTurboIdleId())
        loadComboboxIndex = self.comboBoxCPUTurboLoadState.findData(config.getCPUTurboLoadId())

        self.comboBoxCPUTurboIdleState.setCurrentIndex(idleComboboxIndex)
        self.comboBoxCPUTurboLoadState.setCurrentIndex(loadComboboxIndex)

    @logger.log
    def switchStatisticsBlock(self, is_checked):
        if is_checked:
            new_state = True
        else:
            new_state = False

        self.labelBackupInterval.setEnabled(new_state)
        self.labelBackupIntervalHint.setEnabled(new_state)
        self.spinBoxBackupInterval.setEnabled(new_state)

    @logger.log
    def switchAutostartBlock(self, is_checked):
        if is_checked:
            new_state = True
        else:
            new_state = False

        self.labelAutostartDelay.setEnabled(new_state)
        self.labelAutostartDelayHint.setEnabled(new_state)
        self.spinBoxAutostartDelay.setEnabled(new_state)

    @logger.log
    def switchCPUManagmentBlock(self, is_checked):
        if is_checked:
            new_state = True
        else:
            new_state = False

        self.labelCPUThreshhold.setEnabled(new_state)
        self.spinBoxCPUThreshhold.setEnabled(new_state)

        self.labelCPUIdleState.setEnabled(new_state)
        self.spinBoxCPUIdleState.setEnabled(new_state)

        self.labelCPULoadState.setEnabled(new_state)
        self.spinBoxCPULoadState.setEnabled(new_state)
        self.labelCPULoadStateHint.setEnabled(new_state)

        self.checkBoxCPUTurboManagment.setEnabled(new_state)
        self.labelCPUTurboIdleState.setEnabled(new_state)
        self.comboBoxCPUTurboIdleState.setEnabled(new_state)
        self.labelCPUTurboLoadState.setEnabled(new_state)
        self.comboBoxCPUTurboLoadState.setEnabled(new_state)

    @logger.log
    def closeWindow(self):
        #Локализация
        self.config.setCurrentLanguageCode(self.comboBoxLanguage.currentData())

        #Базовые настройки
        self.config.setCollectSlowDataInterval(float(self.spinBoxLoggingInterval.value()))
        self.config.setCloseToTray(self.checkBoxCloseToTray.isChecked())
        self.config.setOpenMinimized(self.checkBoxOpenMinimized.isChecked())

        #Автозагрузка
        self.config.setAutostartIsActive(self.checkBoxAutostartIsActive.isChecked())
        self.config.setAutostartDelay(int(self.spinBoxAutostartDelay.value()))

        #Статистика
        self.config.setIsBackupNeeded(self.checkBoxStoreStat.isChecked())
        self.config.setBackupInterval(float(self.spinBoxBackupInterval.value()))
        
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