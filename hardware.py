#!/usr/bin/env python3
#Для работы с оборудованием
from types import NoneType
import clr # the pythonnet module.
import subprocess
from subprocess import Popen, PIPE

clr.AddReference(r'./DLL/LibreHardwareMonitorLib') 
clr.FindAssembly(r'./DLL')
from LibreHardwareMonitor.Hardware import Computer

import Entities

#Вот эти пляски со startupinfo нужны, чтобы окно не теряло фокус в процессе запуска подпроцессов
startupinfo = None
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

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

def getCoresAndThreadsCount():
    data = {
            'status' : Entities.Status.not_collect,
            'cores_count' : 0,
            'threads_count' : 0
           }

    #Идем по сенсорам
    for hardware in c.Hardware:
        hardware.Update()

        for sensor in hardware.Sensors:
            #Считаем ядра процессора
            if str(sensor.SensorType) == 'Clock' and 'Core' in str(sensor.Name):
                data['cores_count'] += 1
                continue 

            #Считаем потоки проца
            if str(sensor.SensorType) == 'Load' and 'CPU Core' in str(sensor.Name):
                data['threads_count'] += 1
                continue
                
    if data['cores_count'] == 0:
         data['status'] = Entities.Status.error
    else:
        data['status'] = Entities.Status.success
    
    return data

def collectData(data_lists, cpu_cores, cpu_threads):
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
                new_data = round(sensor.Value, 2)

                general_temps = data_lists['general_temps'][:1]

                if len(general_temps) > 0:
                    old_data = general_temps[0]
                    data['cpu']['temp'] = compareAndGetCorrectSensorDataBetweenOldAndNew(new_data, old_data)
                else:
                    data['cpu']['temp'] = new_data

                continue

            #Добавляем TDP
            if str(sensor.SensorType) == 'Power' and str(sensor.Name) in ('Package', 'CPU Package') and type(sensor.Value) != NoneType:
                new_data = round(sensor.Value, 2)

                general_TDPs = data_lists['general_TDP'][:1]

                if len(general_TDPs):
                    old_data = general_TDPs[0]
                    data['cpu']['tdp'] = compareAndGetCorrectSensorDataBetweenOldAndNew(new_data, old_data)
                else:
                    data['cpu']['tdp'] = new_data

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
                    
    if cpu_threads != 0:
        all_load = all_load/cpu_threads
    else:
        all_load = all_load/cpu_cores

    data['all_load'] = all_load

    return data

def compareAndGetCorrectSensorDataBetweenOldAndNew(new_data, old_data):
    if new_data > old_data*3:
        return old_data*1.5
    else:
        if new_data >= 0.1:
            return new_data
        else:
            return old_data

def setCpuPerformanceState(config, data_lists):
    if not config.getIsCPUManagmentOn():
        return

    #Надо проверить, если последние несколько записей были из режима простоя — значит его можно активировать
    #Это надо, чтобы процессор туда-сюда не дергать постоянно
    data = data_lists['all_load'][:config.getCPUIdleStatePause()]

    if len(list(filter(lambda all_load: (all_load < config.getCPUThreshhold()), data))) == config.getCPUIdleStatePause():
        percentage = config.getCPUIdleState()
        turbo_id = config.getCPUTurboIdleId()
        CPU_performance_mode = False
    else:
        if len(data) > 0:
            if int(data[0]) > int(config.getCPUThreshhold()):
                percentage = config.getCPULoadState()
                turbo_id = config.getCPUTurboLoadId()
                CPU_performance_mode = True
            else:
                CPU_performance_mode = config.getPerformanceCPUModeOn()
        else:
                CPU_performance_mode = config.getPerformanceCPUModeOn()

    if config.getPerformanceCPUModeOn() == CPU_performance_mode:
        return CPU_performance_mode

    setCPULimits(percentage)
    setCPUTurbo(turbo_id)

    return CPU_performance_mode

def setCPUStatetoDefault():
    setCPULimits(100)

def setTurboToDefault():
    setCPUTurbo(2)

def updateCPUParameters(config, idle_state, load_state, idle_id, load_id):
    if config.getPerformanceCPUModeOn() == False and config.getCPULoadState() != idle_state:
        setCPULimits(idle_state)
        setCPUTurbo(idle_id)

    if config.getPerformanceCPUModeOn() == True and config.getCPULoadState() != load_state:
        setCPULimits(load_state)
        setCPUTurbo(load_id)

def setCPULimits(percentage):
    subprocess.run('powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX ' + 
                    str(percentage), startupinfo=startupinfo)

    subprocess.run('powercfg -setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX ' + 
                    str(percentage), startupinfo=startupinfo)

    applyPowerPlanScheme()

def setCPUTurbo(id):
    turbo_statuses = Entities.TurboStatuses()
    mode_index = turbo_statuses.getIndexById(id)

    subprocess.run('powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE ' + 
                    mode_index, startupinfo=startupinfo)

    subprocess.run('powercfg -setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE ' + 
                    mode_index, startupinfo=startupinfo)

    applyPowerPlanScheme()

def applyPowerPlanScheme():
    subprocess.run('powercfg.exe -S SCHEME_CURRENT', startupinfo=startupinfo)

if __name__ == "__main__":
    print(applyPowerPlanScheme())