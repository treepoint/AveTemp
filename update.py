from bs4 import BeautifulSoup
import urllib.request
from langdetect import detect

github_url = 'https://github.com'
maintainer = 'treepoint'

#Со страницы тегов релизов получим все ссылки на релизы
def findLatestReleaseUrl(self):
    soup = BeautifulSoup(urllib.request.urlopen(f'{github_url}/{maintainer}/{self.config.getName()}/tags').read(), 'html.parser')

    release_link = soup.find_all('a', {'class': 'Link--primary'})[0].get('href')

    return f'{ github_url }{ release_link }'

#Соберем всю доп.информацию по релизу
def findReleaseInfo(self):
    release_url = findLatestReleaseUrl(self)

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
                    'download_link' : ''
                    }

    soup = BeautifulSoup(urllib.request.urlopen(release_url).read(), 'html.parser')

    #Найдем основной контент и подтянем из него вложенные элементы
    content_body = soup.find_all('div', {'data-test-selector': 'body-content'})
    contents = content_body[0].contents

    for content in contents:
        if content.name == 'p':
            text = content.getText()

            if len(text) > 0:
                if detect(text) == 'en':
                    release_info['en']['description'] += text
                else:
                    release_info['ru']['description'] += text

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

    release_info['version'] = release_url.replace(f'{github_url}/{maintainer}/{self.config.getName()}/releases/tag/','')
    release_info['download_link'] = f'{github_url}/{maintainer}/{self.config.getName()}/releases/download/{ release_info["version"] }/{self.config.getName()}.exe'

    return release_info

def getVersionHash(version):
    hash = 0
    for number in version.split('.'):
        hash += int(number)

    return hash

def getNewerReleaseInfo(self):
    release_info = findReleaseInfo(self)

    if getVersionHash(release_info['version']) > getVersionHash(self.config.getVersion()):
        release_info['update'] = True
    else:
        release_info['update'] = False

    return release_info

if __name__ == '__main__':
    print(getVersionHash('1.4.3'))