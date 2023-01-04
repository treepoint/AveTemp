# Intro

- English description — https://github.com/treepoint/AveTemp#avetemp-eng
- Русское описание — https://github.com/treepoint/AveTemp#avetemp-ru

# AveTemp (ENG)
AveTemp is software based on python and LibreHardwareMonitorLib for continuous monitoring temperature and TDP of CPU, and for auto setup the CPU performance state and CPU Turbo mode, depends on current load.

<img src="https://user-images.githubusercontent.com/25937222/210169684-56e2132d-5861-4124-ba07-c7d4c1f36c03.jpg" width="702">

It will be helpful to:

- find out how new thermal paste/pads or hardware improvements changed CPU temps into 1, 5, 15, 60 minutes, 24 hours
- increase battery work time
- reduce temps and TDP in idle state and gaming
- reduce carbon emissions
- reduce noise from CPU cooler

## Features
- Continuous monitoring temperature and TDP of CPU
- Collecting and showing min, max and current temps and TDP states
- Collecting and showing average scores for 1, 5, 15, 60 minutes and 24 hours
- Automatic change CPU performance state and CPU Turbo mode. Also, you can setup preferred CPU load threshold, Turbo modes and CPU states or disable it at all.
- Autostart on logon
- Automatic changing the color of tray font for dark and light Windows mode. It's checking on AveTemp restart and every 5 minutes.
- Low CPU usage. For Ryzen 4600H it's < 1% on the peak, most of the time — 0.01%.

Basically, it was developed for notebooks but may help with desktop CPUs too. Tested with:

- Ryzen 4600H
- Ryzen 4800H
- Intel Pentium Gold 7505

And win10/11.

If you have issues with AveTemp on your CPU/system please contact me: https://t.me/PaulKhoziashev, you can write me english or russian. Also, you can send me the issue here: https://github.com/treepoint/AveTemp/issues

## Download

Current release see here: https://github.com/treepoint/AveTemp/releases

## Build and run
For the running:
+ Install Python > 3.10 and PIP
+ Download the latests AveTemp sources
+ Install requirements with pip: pip install -r requirements.txt
+ Run: py AveTemp.py

For the building:
+ Run «auto-py-to-exe»: auto-py-to-exe
+ Into opened window go to «Settings» sections, then click on to «Import Config From JSON File»
+ Choose config file «auto-py-to-exe.config.json»
+ Change addition files locations into sections: «Script Location», «Icon», «Additional Files» and «Output Directory»
+ Run convertation.

## Thanks
I am very appreciating LibreHardwareMonitor and everyone whom working on it https://github.com/LibreHardwareMonitor/LibreHardwareMonitor. Without this library development of AveTemp will be impossible. 

## License
MPL-2.0 license, so you can use it everywhere if you want to without any payments.

## Donate
I will be happy if you will send me money for a coffee cup:

- Uzbek sum: 8600 4904 8192 1298
- USD: 4278 3100 2282 7059
- Russian rubles: 2202 2023 3862 1422

# AveTemp (RU)
AveTemp — программа на базе python и LibreHardwareMonitorLib для непрерывного мониторинга температуры и TDP процессора, а также для автоматической настройки производительности процессора и режима турбо  в зависимости от текущей нагрузки.

<img src="https://user-images.githubusercontent.com/25937222/210169684-56e2132d-5861-4124-ba07-c7d4c1f36c03.jpg" width="702">

Будет полезная если хочется:

- узнать, как новые термопасты/прокладки или аппаратные улучшения изменили температуру процессора за 1, 5, 15, 60 минут, 24 часа
- увеличить время работы от батареи
- снизить температуру и TDP в режиме простоя и в играх
- уменьшить шум от кулера
- снизить выбросы углекислого газа

## Функциональность
- Непрерывный мониторинг температуры и TDP процессора
- Сбор и отображение минимальных, максимальных и текущих значений температуры и TDP
- Сбор и отображение средних показателей за 1, 5, 15, 60 минут и 24 часа
- Автоматическое изменение состояния производительности процессора, режима турбо. Кроме того, все настраивается: порог загрузки процессора, целевые состояния процессора, турбо. Или управление процессором можно отключить вовсе.
- Автозапуск при входе в систему
- Автоматическое изменение цвета шрифта в трее для темного и светлого режима Windows. Проверяется при перезагрузке AveTemp и каждые 5 минут.
- Низкое использование процессора. Для Ryzen 4600H это < 1% максимум, а большую часть времени - 0,01%.

В основном разрабатывал для ноутбуков, однако может быть полезно и для настольных CPU. Протестировано с:

- Ryzen 4600H
- Ryzen 4800H
- Intel Pentium Gold 7505

на win10/11.

Если обнаружите проблемы при работе на вашем процессоре/системе, пожалуйста, свяжитесь со мной: https://t.me/PaulKhoziashev. Еще можно описать проблему здесь: https://github.com/treepoint/AveTemp/issues

## Загрузка

Текущий релиз есть здесь: https://github.com/treepoint/AveTemp/releases

## Сборка и запуск
Для запуска:
+ Установите Python > 3.10 и PIP
+ Скачайте последние исходники AveTemp
+ Установите требования с помощью pip: pip install -r requirements.txt
+ Запустите: py AveTemp.py

Для сборки:
+ Запустите "auto-py-to-exe": auto-py-to-exe
+ В открывшемся окне перейдите в раздел "Settings", затем нажмите на "Import Config From JSON File"
+ Выберите файл конфигурации "auto-py-to-exe.config.json"
+ Измените расположение дополнительных файлов в разделах: "Script Location", "Icon", "Additional Files" и "Output Directory"
+ Запустите конвертацию

## Благодарности
Я очень благодарен LibreHardwareMonitor и всем, кто над ней работает https://github.com/LibreHardwareMonitor/LibreHardwareMonitor. Без этой библиотеки разработка AveTemp будет невозможна. 

## Лицензия
Лицензия MPL-2.0, так что вы можете использовать программу бесплатно везде где если захотите.

## Донаты и поддержка
Я буду рад, если вы скините мне деньги на чашку кофе:

- Узбекские сумы: 8600 4904 8192 1298
- Доллары: 4278 3100 2282 7059
- Российские рубли: 2202 2023 3862 1422
