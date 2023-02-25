import localization
import support
trans = localization.trans

def getAlertsStyles(type):
    if type == 'ERROR':
        header_color = '#fcd2d2'
        main_background = '#fef0f0'
        main_color = '#2f0202'
        scroll_color = 'rgb(252, 143, 156)'
    
    if type == 'INFO':
        header_color = '#d2e0fc'
        main_background = "#f4f7fd"
        main_color = "#020d2f"
        scroll_color = 'rgb(143, 180, 252)'

    if type == 'SUCCESS':
        header_color = '#d2fcd3'
        main_background = "#f0fdf0"
        main_color = "#032f02"
        scroll_color = 'rgb(146, 252, 143)'

    styles = { 
                'alert' : '',
                'description' : ''
             }

    styles['alert'] = f'background: { header_color }; color: { main_color };'

    styles['description'] = ("""
                            QScrollBar:vertical {
                                    width:4px;
                                    margin: 0px 0px 0px 0px;
                            }

                            QScrollBar::handle:vertical {
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop: 0 """ + scroll_color + """, stop: 0.5 """ + scroll_color + """, stop:1 """ + scroll_color + """);
                                    min-height: 0px;
                            }
                            QScrollBar::add-line:vertical {
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop: 0 """ + scroll_color + """, stop: 0.5 """ + scroll_color + """,  stop:1 """ + scroll_color + """);
                                    height: 0px;
                                    subcontrol-position: bottom;
                                    subcontrol-origin: margin;
                            }
                            QScrollBar::sub-line:vertical {
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop: 0  """ + scroll_color + """, stop: 0.5 """ + scroll_color + """,  stop:1 """ + scroll_color + """);
                                    height: 0 px;
                                    subcontrol-position: top;
                                    subcontrol-origin: margin;
                            }
                            QPlainTextEdit { 
                                background: """ + main_background + """; 
                                margin-left: 1px; 
                                color: """ + main_color + """; 
                                padding: 4px;
                            }
                    """)
    
    return styles

def setAlert(self, type = 'INFO', locale_text_alert = 'ERROR', description_text = False):
    if (self.is_alert_showing):
        self.frameAlert.setVisible(False)
        self.is_alert_showing = False

    styles = getAlertsStyles(type)

    self.frameAlert.setStyleSheet(styles['alert'])
    self.plainTextEditAlert.setStyleSheet(styles['description'])

    setAlertTextAndShow(self, locale_text_alert)

    if (description_text):
        setAlertDescriptionText(self, description_text)
        expandAlert(self)

def setAlertTextAndShow(self, locale_text):
    #Получим локализацию
    locale = self.config.getCurrentLanguageCode()
    #Запишем текст алерта для перевода на лету
    self.config.setAlertText(locale_text)
    #Проставим локализованный
    init_trans = localization.initTrans(self.localizations)
    self.labelAlert.setText(trans(locale, locale_text, init_trans))
    #Покажем
    self.frameAlert.setVisible(True)
    self.is_alert_showing = True
    #Компенсируем размеры окна, учитывая открытый алерт
    support.setWindowsSize(self)

def setAlertDescriptionText(self, text):
    self.plainTextEditAlert.setPlainText(text)

def expandAlert(self):
    support.setWindowsSize(self, 72)
    self.widgetCurrentValues.setVisible(False)
    self.plainTextEditAlert.setVisible(True)

def minimizeAlert(self):
    self.widgetCurrentValues.setVisible(True)
    self.plainTextEditAlert.setVisible(False)