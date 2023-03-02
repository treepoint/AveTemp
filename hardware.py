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

def initHardware():
    #Подрубаем общий мониторинг на всю сессию
    computer = Computer()
    #Включаем сбор информации по процу
    computer.IsCpuEnabled = True 
    computer.Open()

    return computer

def closeHardware(computer):
    computer.Close()

def getCpuName(computer):
    #Идем по сенсорам и забираем название проца
    for hardware in computer.Hardware:
        if 'LibreHardwareMonitor.Hardware.CPU' in str(hardware.GetType()):
            name = str(hardware.Name)
            if 'with' not in name:
                cpu_name = name
            else:
                cpu_name, graphics = str(hardware.Name).split(' with') 
            
            intel_gen_index = cpu_name.find('Gen')

            if intel_gen_index > 0:
                cpu_name = cpu_name.split('Gen ',1)[1]
            
            return cpu_name

def getCoresAndThreadsCount(computer):
    data = {
            'status' : Entities.Status.not_collect,
            'cores_count' : 0,
            'threads_count' : 0
           }

    #Идем по сенсорам
    for hardware in computer.Hardware:
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

def collectFastData(computer, data_lists, cpu_threads):
    data = {
            'status' : Entities.Status.not_collect,
            'all_load' : 0,
            'cpu' : 
                    {
                    'threads' : [],
                    }
           }

    all_load = 0

    for hardware in computer.Hardware:
        hardware.Update()

        for sensor in hardware.Sensors:

            #Добавляем загрузку в рамках логических ядер проца
            if str(sensor.SensorType) == 'Load' and 'CPU Core' in str(sensor.Name):
                sensors = str(sensor.Name).split('#')

                #костыль для Intel
                if len(sensors) == 3:
                    number = sensors[2]
                else:
                    number = sensors[1]

                #Усредним значение нагрузки, чтобы единичные скачки не приводили к преждевременному бустоизвержению
                threads = data_lists['cpu']['threads']

                new_data = sensor.Value

                if len(threads) > 0:
                    old_data = float(threads[int(number)-1]['load'])
                    core_load = compareAndGetCorrectSensorDataBetweenOldAndNew(new_data, old_data)
                else:
                    core_load = new_data

                core_load = round(core_load, 2)

                all_load += core_load
                
                data['cpu']['threads'] += [{'id' : int(number), 'load' : core_load}]
    
    data['all_load'] = round(all_load/cpu_threads, 2)

    if data['all_load'] == 0:
         data['status'] = Entities.Status.error
    else:
        data['status'] = Entities.Status.success

    return data

def collectSlowData(computer, data_lists):
    data = {
            'status' : Entities.Status.not_collect,
            'cpu' : 
                    {
                    'temp' : 0, 
                    'tdp' : 0, 
                    'cores' : [],
                    }
           }

    #Идем по сенсорам
    for hardware in computer.Hardware:
        hardware.Update()

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
                    
    if len(general_temps) == 0:
         data['status'] = Entities.Status.error
    else:
        data['status'] = Entities.Status.success

    return data

def compareAndGetCorrectSensorDataBetweenOldAndNew(new_data, old_data, smoothing_factor = 1.5, theshold = 3):
    if new_data > old_data*theshold:
        return new_data/smoothing_factor

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

    idle_ticks_count = len(list(filter(lambda all_load: (all_load < config.getCPUThreshhold()), data)))
    turbo_ticks = list(filter(lambda all_load: (all_load >= config.getCPUThreshhold()), data[:3]))[::-1]

    if idle_ticks_count == config.getCPUIdleStatePause():
        percentage = config.getCPUIdleState()
        turbo_id = config.getCPUTurboIdleId()
        CPU_performance_mode_on = False
    else:
        if (len(turbo_ticks) >= 2):
            #Врубаем турбо или если прошло 3 турбо тика или если второй тик больше первого на 15%
            #Так пытаемся минимизировать лишнее включение турбо когда не надо
            if (len(turbo_ticks) >= 3) or (turbo_ticks[1] >= turbo_ticks[0] + 15):
                if int(data[0]) > int(config.getCPUThreshhold()):
                    percentage = config.getCPULoadState()
                    turbo_id = config.getCPUTurboLoadId()
                    CPU_performance_mode_on = True

                #Во всех других случаях ничего не меняем и возвращаем как есть
                else:
                    CPU_performance_mode_on = config.getPerformanceCPUModeOn()
            else:
                CPU_performance_mode_on = config.getPerformanceCPUModeOn()
        else:
            CPU_performance_mode_on = config.getPerformanceCPUModeOn()

    #Если мы уже в нужном режиме — не переключаем
    if config.getPerformanceCPUModeOn() == CPU_performance_mode_on:
        return CPU_performance_mode_on

    setCPULimits(percentage)

    if config.getIsTurboManagmentOn():
        setCPUTurbo(turbo_id)

    return CPU_performance_mode_on

def setCPUStatetoDefault():
    setCPULimits(100)

def setTurboToDefault():
    setCPUTurbo(2)

def updateCPUParameters(self, current_config):
    if not current_config.getIsCPUManagmentOn():
        return

    #Получим новые состояния
    new_idle_state = self.config.getCPUIdleState()
    new_load_state = self.config.getCPULoadState()
    new_idle_id = self.config.getCPUTurboIdleId()
    new_load_id = self.config.getCPUTurboLoadId()

    #Получим старые состояния
    current_idle_state = current_config.getCPUIdleState()
    current_load_state = current_config.getCPULoadState()
    current_idle_id = current_config.getCPUTurboIdleId()
    current_load_id = current_config.getCPUTurboLoadId()
    cpu_performance_mode_on = current_config.getPerformanceCPUModeOn()

    #Сравним состояния и применим если надо
    if cpu_performance_mode_on == False:
        if current_idle_state != new_idle_state:
            setCPULimits(new_idle_state)
        if current_idle_id != new_idle_id:
            setCPUTurbo(new_idle_id)

    if cpu_performance_mode_on == True:
        if current_load_state != new_load_state:
            setCPULimits(new_load_state)
        if current_load_id != new_load_id:
            setCPUTurbo(new_load_id)

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

def getAvgTempForSeconds(self, collect_slow_data_interval):
    average_temps_sum_perion = sum(self.data_lists['average_temps'][:collect_slow_data_interval*self.collect_koef])
    average_temps_len_perion = len(self.data_lists['average_temps'][:collect_slow_data_interval*self.collect_koef])

    return average_temps_sum_perion/average_temps_len_perion

def getAvgTDPForSeconds(self, collect_slow_data_interval):
    average_TDPs_sum_perion = sum(self.data_lists['average_TDP'][:collect_slow_data_interval*self.collect_koef])
    average_TDPs_len_perion = len(self.data_lists['average_TDP'][:collect_slow_data_interval*self.collect_koef])

    return average_TDPs_sum_perion/average_TDPs_len_perion

def checkSMT(self):
    return self.cpu_cores != self.cpu_threads

if __name__ == "__main__":
    collectFastData()