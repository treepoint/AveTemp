from PIL import Image, ImageDraw, ImageFont, ImageQt
from PyQt6.QtGui import QPixmap
import configparser  # Для чтения конфига
import ctypes
import os, sys
import json

from pathlib import Path

import Entities 

config_file = 'settings.ini'
stat_file = 'stat.json'

## Эта функция нужна, потому что auto-py-to-exe с какого-то времени хочет абсолютные пути для картинок и прочего
## Тогда как я хочу относительные, по крайней мере для этапа разработки. Так что она просто в нужных местах меняет.

## Разумеется это значит, что если в интерфейсных файлах хочется абсолютные пути, то там надо ручками после QT designer менять
## Например, чтобы было вот так —   "    border-image: url("+ support.resource_path('./images/settings.png')+ ");\n"
def resource_path(relative_path):
    path = Path(relative_path)

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    path = str(os.path.join(base_path, path))
    path = path.replace('\\', '/')
    path = path[0:2] + '/' + path[2:]

    return path

def to_round_str(value):
    return str(round(value,1))

def check_admin_right():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()

    return is_admin

def createEmptyConfigFile():
    config = Entities.Config()

    configParser = configparser.ConfigParser()

    configParser['main'] = {'collect_interval': config.get_collect_interval(), 
                            'store_period': config.get_store_period(),
                            'is_backup_needed' : config.get_is_backup_needed(),
                            'close_to_tray': config.get_close_to_tray(),
                            'open_minimized': config.get_open_minimized()}

    with open(config_file, 'w') as configfile:
        configParser.write(configfile)


def writeToConfig(self, config):

    configParser = configparser.ConfigParser()

    configParser['main'] = {'collect_interval': config.collect_interval, 
                            'store_period': config.store_period,
                            'is_backup_needed' : config.get_is_backup_needed(),
                            'close_to_tray': config.close_to_tray,
                            'open_minimized': config.open_minimized}

    with open(config_file, 'w') as configfile:
        configParser.write(configfile)

def to_bool(value):
    if type(value):
        if str(value) == 'False':
            return False
        else:
            return True
    else:
        if int(value) == 0:
            return False
        else:
            return True  

def readConfig(self):
    config = configparser.ConfigParser()

    if len(config.read(config_file)) != 1:
        createEmptyConfigFile()
        config.read(config_file)

    self.config.set_collect_interval(float(config['main']['collect_interval']))
    self.config.set_store_period(int(config['main']['store_period']))
    self.config.set_is_backup_needed(to_bool(config['main']['is_backup_needed']))
    self.config.set_close_to_tray(to_bool(config['main']['close_to_tray']))
    self.config.set_open_minimized(to_bool(config['main']['open_minimized']))

#Получаем картинку для трея
def get_tray_image(value):
    value = float(value)
        
    #Делаем базовое изображение с прозрачным фоном
    image = Image.new('RGBA', (100, 100), color = (255, 255, 255, 0))

    #Создаем изображение
    dc = ImageDraw.Draw(image)

    #Задаем шрифт
    font_type  = ImageFont.truetype("arial.ttf", 82)

    #Округляем значение и отрисовываем
    text = round(value)
    dc.text((6,6), f"{text}", fill=(255,255,255), font = font_type)

    imageQT = ImageQt.ImageQt(image)

    pixmap = QPixmap.fromImage(imageQT)

    return pixmap

def save_data(data):

    jsonStr = json.dumps(data)

    with open(stat_file, 'w') as bf:
        bf.write(jsonStr)

def remove_stat_file():
    os.remove(stat_file)

def get_restored_data():

    data = False

    try:
        file = open(stat_file)
        data = json.load(file)
    except:
        return data

    return data