#!/usr/bin/env python3
#Для работы с оборудованием
from types import NoneType
import clr # the pythonnet module.

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
            cpu_name, graphics = str(hardware.Name).split(' with') 
            return cpu_name

def collectData():
    #Обновляем значения
    #c.Reset() 

    data = {
            'status' : Entities.Status.not_collect,
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
        for sensor in hardware.Sensors:
            #Добавляем общую температуру проца
            if str(sensor.SensorType) == 'Temperature' and str(sensor.Name) == 'Core (Tctl/Tdie)':
                data['cpu']['temp'] = round(sensor.Value, 2)

            #Добавляем TDP
            if str(sensor.SensorType) == 'Power' and str(sensor.Name) == 'Package' and type(sensor.Value) != NoneType:
                data['cpu']['tdp'] = round(sensor.Value, 2)

            #Добавляем частоты в рамках физических ядер проца
            if str(sensor.SensorType) == 'Clock' and 'Core' in str(sensor.Name):
                name, number = str(sensor.Name).split('#')
                data['cpu']['cores'] += [{'id' : int(number), 'clock' : round(sensor.Value,2)}]

            #Добавляем загрузку в рамках логических ядер проца
            if str(sensor.SensorType) == 'Load' and 'CPU Core' in str(sensor.Name):
                name, number = str(sensor.Name).split('#')
                data['cpu']['threads'] += [{'id' : int(number), 'load' : round(sensor.Value,2)}]
                
    if len(data['cpu']['cores']) == 0:
         data['status'] = Entities.Status.error
    else:
        data['status'] = Entities.Status.success

    return data

if __name__ == "__main__":
    data = collectData()

    print(data)