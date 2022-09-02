from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QThread, pyqtSignal
import sys
import time

import MainWindow

class Worker(QThread):
    result = pyqtSignal(str)

    def __init__(self, collect_interval):
        super().__init__()

        self.collect_interval = collect_interval

    def run(self):
        self.keepRunning = True
        while self.keepRunning:
            time.sleep(self.collect_interval)
            self.result.emit('')

    def stop(self):
        self.keepRunning = False

class TrayWrapper:
    def __init__(self):
        self.app = QApplication(sys.argv)
        #Схлопываем трей когда закрываем основное окно
        self.app.setQuitOnLastWindowClosed(True)

        self.window = MainWindow.Main()
        self.window.resize(300, 300)

        icon = QIcon(self.window.image)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)

        if self.window.config.open_minimized:
            self.window.hide()
        else:
            self.window.show()

        self.collect_interval = self.window.collect_interval

        #Меню
        menu = QMenu()
        #Набор пунктов
        action = QAction('Выйти')
        menu.addAction(action)
        action.triggered.connect(self.app.quit)

        self.tray.setContextMenu(menu)

        #Обработка событий
        self.tray.activated.connect(self.onTrayIconActivated)

        #Создаем поток для обновления информации в трее
        self.worker = Worker(self.collect_interval)
        self.worker.result.connect(self.update_icon)
        self.worker.start()

        #Ну и запускаем
        self.app.exec()

    def update_icon(self):
        icon = QIcon(self.window.image)
        self.tray.setIcon(icon)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.window.showNormal()

if __name__ == "__main__":
    app = TrayWrapper()