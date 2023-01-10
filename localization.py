from pyi18n.loaders import PyI18nBaseLoader

import Entities

class Loader(PyI18nBaseLoader):
    def load(self, locales: tuple):
        self.localization = Entities.Localizations
        return self.localization.getDictionary()