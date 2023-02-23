from pyi18n.loaders import PyI18nBaseLoader
from pyi18n import PyI18n

import Entities
import locale

localizations = Entities.Localizations()
languages = Entities.Languages()
config = Entities.Config()

class Loader(PyI18nBaseLoader):
    def __init__(self, load_path: str, localizations):
        self.localizations = localizations
        self.load_path = load_path

    def load(self, load_path: str):
        return self.localizations.getDictionary()

def getCurrentSystemLanguage():
    loc = locale.getdefaultlocale()[0]

    languages = Entities.Languages()

    if 'ru' in loc:
        return languages.getRussian()
    else:
        return languages.getEnglish()

def initTrans(localizations):
    #Обязательно хочет path, потому что ищет файлы. Удачи ему.
    #Я ченкул исходный код, там проверяется конкретный файл в конкретном месте
    #Если его нет — просто continue, так что бог с ним
    loader = Loader(load_path="/", localizations = localizations)

    #Инициализируем и адаптируем
    i18n = PyI18n(('en', 'ru'), loader=loader)
    trans = i18n.gettext

    return trans

init_trans = initTrans(localizations = localizations)

def trans(locale, phrase, init_trans = init_trans):
    return init_trans(locale, phrase)