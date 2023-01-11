from pyi18n.loaders import PyI18nBaseLoader
from pyi18n import PyI18n

import Entities
import locale

localizations = Entities.Localizations()
languages = Entities.Languages()
config = Entities.Config()

class Loader(PyI18nBaseLoader):
    def load(self, load_path: str):
        return localizations.getDictionary()

#Обязательно хочет path, потому что ищет файлы. Удачи ему
#Я ченкул исходный код, там проверяется конкретный файл в конкретном месте
#Если его нет — просто continue, так что бог с ним
loader = Loader(load_path="/")

def getCurrentSystemLanguage():
    loc = locale.getdefaultlocale()[0]

    languages = Entities.Languages()

    if 'ru' in loc:
        return languages.getRussian()
    else:
        return languages.getEnglish()

def initTrans():
    #Инициализируем и адаптируем
    #TODO: поправить с конфигом
    i18n = PyI18n(('en', 'ru'), loader=loader)
    trans = i18n.gettext

    return trans

init_trans = initTrans()

def trans(locale, phrase):
    result = init_trans(locale, phrase)

    return result