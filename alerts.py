import localization
import support
import Entities

trans = localization.trans
languages = Entities.Languages()

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

def setAlert(self, type = 'INFO', locale_text_alert = False, locale_description_text = False):
    if not locale_text_alert:
        return

    locale_list = languages.getList()

    #Переопредим заголовок алерта
    for locale in locale_list:
        text = trans(locale, locale_text_alert)
        self.localizations.setDictionaryValue(locale, 'alert_title', text)

    if (self.is_alert_showing):
        self.frameAlert.setVisible(False)
        self.is_alert_showing = False

    #Зададим стили
    styles = getAlertsStyles(type)
    self.frameAlert.setStyleSheet(styles['alert'])

    #Зададим текстовки
    self.labelAlert.setText(trans(self.locale, locale_text_alert))

    #Покажем
    self.frameAlert.setVisible(True)
    self.is_alert_showing = True

    #Если есть — зададим
    if (locale_description_text):
        #Переопредим описание алерта
        for locale in locale_list:
            text = trans(locale, locale_description_text)
            self.localizations.setDictionaryValue(locale, 'alert_description', text)
            
        self.plainTextEditAlert.setStyleSheet(styles['description'])
        self.plainTextEditAlert.setPlainText(trans(self.locale, locale_description_text))
        self.buttonAlertExpand.setVisible(True)

def setExpandAlertButtonStyle(self):
    if self.is_alert_expand:
        image = 'expand'
    else:
        image = 'minimize'
    
    self.buttonAlertExpand.setStyleSheet("QPushButton {\n"
                                        "    qproperty-icon: none;\n"
                                        "    qproperty-iconSize: 18px;\n"
                                        "    image : url("+ support.getResourcePath('./images/' + image + '.svg')+ ");\n"
                                        "    border-radius: 4px; \n"
                                        "    background: #eeeeee; \n"
                                        "    font-weight: normal; \n"
                                        "    color: #222;\n"
                                        "    padding: 4px; \n"
                                        "    margin-bottom: 1px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "    image : url("+ support.getResourcePath('./images/' + image + '_hover.svg')+ ");\n"
                                        "    background: #d8d8d8; \n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed\n"
                                        "{\n"
                                        "    image : url("+ support.getResourcePath('./images/' + image + '_pressed.svg')+ ");\n"
                                        "    background: #c9c9c9; \n"
                                        "}")

def expandAlert(self):
    if self.is_alert_expand:
        self.plainTextEditAlert.setVisible(False)
        self.is_alert_expand = False
        self.widgetCurrentValues.setVisible(True)
        setExpandAlertButtonStyle(self)
    else:
        self.widgetCurrentValues.setVisible(False)
        self.is_alert_expand = True
        setExpandAlertButtonStyle(self)
        self.plainTextEditAlert.setVisible(True)

def closeAlert(self):
    self.frameAlert.setVisible(False)
    self.is_alert_showing = False
    if self.is_alert_expand:
        expandAlert(self)
    support.setComponentsSize(self)