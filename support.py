from PIL import Image, ImageDraw, ImageFont, ImageQt
from PyQt6.QtGui import QPixmap
import configparser  # Для чтения конфига
import ctypes
import os, sys
import json

from pathlib import Path

import Entities 
import registry
import taskManager

config_file = 'settings.ini'
stat_file = 'statistics.json'

## Эта функция нужна, потому что auto-py-to-exe с какого-то времени хочет абсолютные пути для картинок и прочего
## Тогда как я хочу относительные, по крайней мере для этапа разработки. Так что она просто в нужных местах меняет.

## Разумеется это значит, что если в интерфейсных файлах хочется абсолютные пути, то там надо ручками после QT designer менять
## Например, чтобы было вот так — "border-image: url("+ support.getResourcePath('./images/settings.png')+ ");\n"
def getResourcePath(relative_path):
    path = Path(relative_path)

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    path = str(os.path.join(base_path, path))
    path = path.replace('\\', '/')
    path = path[0:2] + '/' + path[2:]

    return path

def toRoundStr(value):
    return str(round(value, 1))

def isThereAdminRight():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()

    return is_admin

def writeToConfig(config):
    configParser = configparser.ConfigParser()

    #Получим описание раздела main для конфига
    configParser['main'] = Entities.ConfigParser.getMain(config)

    with open(config_file, 'w') as configfile:
        configfile.truncate(0)
        configParser.write(configfile)

def createEmptyConfigFile():
    config = Entities.Config()

    writeToConfig(config)

def toBool(value):
    if isinstance(value, str):
        if str(value) == 'False':
            return False
        else:
            return True

    if isinstance(value, int):
        if int(value) == 0:
            return False
        else:
            return True
    
    return False

def readConfig(self):
    config = configparser.ConfigParser()

    #Проверяем, что файл в наличии
    if len(config.read(config_file)) != 1:
        createEmptyConfigFile()
        config.read(config_file)

    try:
        #Заберем настройки из файла

        #Общие
        self.config.setCollectInterval(float(config['main']['collect_interval']))
        self.config.setStorePeriod(int(config['main']['store_period']))
        self.config.setIsBackupNeeded(toBool(config['main']['is_backup_needed']))
        self.config.setCloseToTray(toBool(config['main']['close_to_tray']))
        self.config.setOpenMinimized(toBool(config['main']['open_minimized']))

        #Управление процессором
        self.config.setIsCPUManagmentOn(toBool(config['main']['is_CPU_managment_on']))
        self.config.setCPUThreshhold(int(config['main']['CPU_threshhold']))
        self.config.setCPUIdleState(int(config['main']['CPU_idle_state']))
        self.config.setCPULoadState(int(config['main']['CPU_load_state']))
        #Управление турбо режимом
        self.config.setIsTurboManagmentOn(toBool(config['main']['is_turbo_managment_on']))
        self.config.setCPUTurboIdleId(int(config['main']['CPU_turbo_idle_id']))
        self.config.setCPUTurboLoadId(int(config['main']['CPU_turbo_load_id']))

        #И, заодно, прочитаем нужные параметры реестра
        self.config.setSystemUsesLightTheme(registry.getCurrentThemeIsLight())

        #И из системных данных windows
        self.config.setAutostartIsActive(taskManager.checkThatAutostartIsActive(self))
    except:
        print('Settings file is corrupted, makes new one')
        createEmptyConfigFile()
        readConfig(self)

    return self.config
    
#Получаем картинку для трея
def getTrayImage(value, config):
    value = float(value)

    is_light_theme = config.getSystemUsesLightTheme()

    #Делаем базовое изображение с прозрачным фоном
    image = Image.new('RGBA', (100, 100), color = (255, 255, 255, 0))

    #Создаем изображение
    dc = ImageDraw.Draw(image)

    #Задаем шрифт
    font_type  = ImageFont.truetype("segoeuisl.ttf", 86)

    #Округляем значение и отрисовываем
    text = round(value)

    if is_light_theme:
        text_color = (25, 25, 25)
    else:
        text_color = (255,255,255)
     
    dc.text((6,-12), f"{text}", fill=text_color, font = font_type)

    imageQT = ImageQt.ImageQt(image)

    pixmap = QPixmap.fromImage(imageQT)

    return pixmap

def saveData(self):
    #Добавляем версию, чтобы проверять на совместимость
    data = self.data_lists
    data['version'] = self.config.getVersion()

    jsonStr = json.dumps(data)

    with open(stat_file, 'w') as bf:
        bf.write(jsonStr)

def removeStatFile():
    os.remove(stat_file)

def getRestoredData(self):

    try:
        file = open(stat_file)
        data = json.load(file)
        file.close()
    except:
        return False

    if 'version' not in data:
        removeStatFile()
        return False
    
    if data['version'] != self.config.getVersion():
        removeStatFile()
        return False
    else:
        data.pop('version')
        return data

def getCurrentPath():
    return os.getcwd()