from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import QThread, pyqtSignal, Qt
import sys
import time
import support

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
        
        app_icon = support.getResourcePath('./images/icon.png')

        self.window.setWindowIcon(QIcon(app_icon))

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
        menu.setFont(QFont('Segoe UI Semilight', 10))
        menu.setStyleSheet("QMenu::item {"
                                        "padding: 2px 12px 2px 12px;"
                                        "}"
                           "QMenu::item:selected {"
                                        "background-color: rgb(225, 225, 225);"
                                        "color: rgb(25, 25, 25);"
                                        "}")

        #Набор пунктов
        action = QAction('Закрыть')
        menu.addAction(action)
        action.triggered.connect(self.app.quit)

        self.tray.setContextMenu(menu)

        #Обработка событий
        self.tray.activated.connect(self.onTrayIconActivated)

        #Создаем поток для обновления информации в трее
        self.worker = Worker(self.collect_interval)
        self.worker.result.connect(self.updateIcon)
        self.worker.start()

        #Ну и запускаем
        self.app.exec()

    def updateIcon(self):
        icon = QIcon(self.window.image)
        self.tray.setIcon(icon)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.window.isHidden():
                self.window.show()
                self.window.setWindowState(Qt.WindowState.WindowActive)
                self.window.setFocus()
            else:
                if self.window.windowState() != Qt.WindowState.WindowActive:
                    self.window.setWindowState(Qt.WindowState.WindowActive)
                    self.window.setFocus()
                else:
                    self.window.hide()

if __name__ == "__main__":
    app = TrayWrapper()