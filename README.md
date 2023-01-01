# AveTemp
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
