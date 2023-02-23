import localization
trans = localization.trans

def setAlertError(self, locale_text='ERROR'):
    self.frameAlert.setStyleSheet(f"background: #fcd2d2; color: #2f0202;")
    setAlertTextAndShow(self, locale_text)

def setAlertInfo(self, locale_text='INFO'):
    self.frameAlert.setStyleSheet(f"background: #d2e0fc; color: #020d2f;")
    setAlertTextAndShow(self, locale_text)

def setAlertSuccess(self, locale_text='SUCCESS'):
    self.frameAlert.setStyleSheet(f"background: #d2fcd3; color: #032f02;")
    setAlertTextAndShow(self, locale_text)

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