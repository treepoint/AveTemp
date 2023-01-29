from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import Qt

import support
import sys
import workers
import MainWindow

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

        if self.window.config.getOpenMinimized():
            self.window.hide()
        else:
            self.window.show()

        self.collect_slow_data_interval = self.window.config.getCollectSlowDataInterval()

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
        action.triggered.connect(self.properQuit)

        self.tray.setContextMenu(menu)

        #Обработка событий
        self.tray.activated.connect(self.onTrayIconActivated)

        #Создаем поток для обновления информации в трее
        self.app_worker = workers.TrayWorker(self)
        self.app_worker.result.connect(self.updateIcon)
        self.app_worker.start()

        #Ну и запускаем
        self.app.exec()

    def properQuit(self):
        self.tray.setVisible(False)
        exit(0)

    def updateIcon(self, result):
        if result:
            icon = QIcon(self.window.image)
            self.tray.setIcon(icon)
        else:
            #Если из воркера не пришел результат — значит приложение закрыли, дропаем
            self.tray.setVisible(False)
            exit(0)

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