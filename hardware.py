#!/usr/bin/env python3
#Для работы с оборудованием
from types import NoneType
import clr # the pythonnet module.
import subprocess

clr.AddReference(r'./DLL/LibreHardwareMonitorLib') 
clr.FindAssembly(r'./DLL')
from LibreHardwareMonitor.Hardware import Computer

import Entities

#Подрубаем общий мониторинг на всю сессию
c = Computer()
#Включаем сбор информации по процу
c.IsCpuEnabled = True 
c.Open()

def getCpuName():
    #Идем по сенсорам и забираем название проца
    for hardware in c.Hardware:
        if 'LibreHardwareMonitor.Hardware.CPU' in str(hardware.GetType()):
            name = str(hardware.Name)
            if 'with' not in name:
                cpu_name = name
            else:
                cpu_name, graphics = str(hardware.Name).split(' with') 
            
            return cpu_name

def collectData(config):
    #Обновляем значения
    #c.Reset() 

    data = {
            'status' : Entities.Status.not_collect,
            'all_load' : 0,
            'cpu': 
                {
                 'temp' : 0, 
                 'tdp' : 0, 
                 'cores' : [],
                 'threads' : [],
                }
           }

    #Идем по сенсорам
    for hardware in c.Hardware:
        hardware.Update()

        all_load = 0

        for sensor in hardware.Sensors:
            #Добавляем общую температуру проца
            if str(sensor.SensorType) == 'Temperature' and str(sensor.Name) in ('Core (Tctl/Tdie)', 'CPU Package'):
                data['cpu']['temp'] = round(sensor.Value, 2)
                continue

            #Добавляем TDP
            if str(sensor.SensorType) == 'Power' and str(sensor.Name) in ('Package', 'CPU Package') and type(sensor.Value) != NoneType:
                data['cpu']['tdp'] = round(sensor.Value, 2)
                continue 

            #Добавляем частоты в рамках физических ядер проца
            if str(sensor.SensorType) == 'Clock' and 'Core' in str(sensor.Name):
                number = str(sensor.Name).split('#')[1]

                if isinstance(sensor.Value, type(None)):
                    value = 0
                else:
                    value = round(sensor.Value, 2)

                data['cpu']['cores'] += [{'id' : int(number), 'clock' : value }]
                continue 

            #Добавляем загрузку в рамках логических ядер проца
            if str(sensor.SensorType) == 'Load' and 'CPU Core' in str(sensor.Name):
                sensors = str(sensor.Name).split('#')

                if len(sensors) == 3:
                    number = sensors[2]
                else:
                    number = sensors[1]

                core_load = round(sensor.Value,2)
                
                data['cpu']['threads'] += [{'id' : int(number), 'load' : core_load}]

                all_load += core_load
                continue
                
    cores_count = len(data['cpu']['cores'])

    if cores_count == 0:
         data['status'] = Entities.Status.error
    else:
        data['status'] = Entities.Status.success
        all_load = all_load/cores_count
        data['all_load'] = all_load

    if all_load < config.CPU_turbo_threshhold:
        setCpuPerformanceStatePercentage(config.CPU_turbo_idle_state)
    else:
        setCpuPerformanceStatePercentage(config.CPU_turbo_load_state)

    return data

def setCpuPerformanceStatePercentage(percentage):
    subprocess.call("powercfg -setacvalueindex SCHEME_BALANCED SUB_PROCESSOR PROCTHROTTLEMAX " + str(percentage))
    subprocess.call("powercfg -setdcvalueindex SCHEME_BALANCED SUB_PROCESSOR PROCTHROTTLEMAX " + str(percentage))

if __name__ == "__main__":
    setCpuPerformanceStatePercentage(100)