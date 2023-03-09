from bs4 import BeautifulSoup
import urllib.request
from langdetect import detect

import alerts
import localization
import Entities
import logger

trans = localization.trans
languages = Entities.Languages()

github_url = 'https://github.com'
maintainer = 'treepoint'

#Со страницы тегов релизов получим все ссылки на релизы
@logger.log
def findLatestReleaseUrl(self):

    soup = BeautifulSoup(urllib.request.urlopen(f'{github_url}/{maintainer}/{self.config.getName()}/tags').read(), 'html.parser')

    release_link = soup.find_all('a', {'class': 'Link--primary'})[0].get('href')

    return f'{ github_url }{ release_link }'

#Соберем всю доп.информацию по релизу
@logger.log
def findReleaseInfo(self):
    release_info = {
                    'version': 0,
                    'en': {
                            'description': '',
                            'release_notes': [],
                            },
                    'ru': {
                            'description': '',
                            'release_notes': [],
                            },
                    'download_link' : '',
                    'ok': False
                    }

    try:
        release_url = findLatestReleaseUrl(self)
    except:
        return release_info

    soup = BeautifulSoup(urllib.request.urlopen(release_url).read(), 'html.parser')
    
    #Найдем основной контент и подтянем из него вложенные элементы
    content_body = soup.find_all('div', {'data-test-selector': 'body-content'})
    contents = content_body[0].contents

    for content in contents:
        if content.name == 'p':
            text = content.getText()

            if len(text) > 0:
                if detect(text) == 'en':
                    release_info['en']['description'] += f'{text}\n\n'
                else:
                    release_info['ru']['description'] += f'{text}\n\n'

        if content.name == 'ul' or content.name == 'ol':
            release_notes = content.contents

            for note in release_notes:
                if note.name == 'li':
                    text = note.getText()
                   
                    if len(text) > 0:
                        if detect(text) == 'en':
                            release_info['en']['release_notes'].append(text.replace('\n',''))
                        else:
                            release_info['ru']['release_notes'].append(text.replace('\n',''))

    #Удалим последние переносы строк
    release_info['en']['description'] = release_info['en']['description'][:-2]
    release_info['ru']['description'] = release_info['ru']['description'][:-2]

    release_info['version'] = release_url.replace(f'{github_url}/{maintainer}/{self.config.getName()}/releases/tag/','')
    release_info['download_link'] = f'{github_url}/{maintainer}/{self.config.getName()}/releases/download/{ release_info["version"] }/{self.config.getName()}.exe'
    release_info['release_url'] = release_url

    release_info['ok'] = True

    return release_info

@logger.log
def getVersionHash(self, version):
    hash = 0
    for number in version.split('.'):
        hash += int(number)

    return hash

@logger.log
def getNewerReleaseInfo(self):
    release_info = findReleaseInfo(self)

    if not release_info['ok']:
        release_info['update'] = False
        return release_info

    if getVersionHash(self, release_info['version']) > getVersionHash(self, self.config.getVersion()):
        release_info['update'] = True
    else:
        release_info['update'] = False

    return release_info

@logger.log
def reorderNewReleaseAlertText(self):
    locale_list = languages.getList()

    for locale in locale_list:
        text = trans(locale, 'new_release')
        text = text.replace('<release_url>', self.release_info['release_url'])
        self.localizations.setDictionaryValue(locale, 'new_release', text)

@logger.log
def updateTransReleaseNotes(self):

    locale_list = languages.getList()

    for locale in locale_list:
        #Соберем описание релиза
        release_notes = ''

        release_length = len(self.release_info[locale]['release_notes'])

        for index, note in enumerate(self.release_info[locale]['release_notes']):
            if (index + 1 != release_length):
                release_notes += f'• { note }\n\n'
            else:
                release_notes += f'• { note }'

        text = f'{self.release_info[locale]["description"]}\n{release_notes}'

        self.localizations.setDictionaryValue(locale, 'new_release_description', text)

@logger.log
def checkUpdates(self):
    #Получим инфу
    self.release_info = getNewerReleaseInfo(self)

    #Если ничего нет — выйдем
    if not self.release_info['update']:
        return
    
    #Зададим локализации текста для алерта
    reorderNewReleaseAlertText(self)
    #Зададим локализации текста для описания алерта
    updateTransReleaseNotes(self)

    #Зададим все и покажем
    alerts.setAlert(self, 'INFO', 'new_release', 'new_release_description')
    return

if __name__ == '__main__':
    print(getVersionHash('1.4.3'))