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
import logger
import support

#Вот эти пляски со startupinfo нужны, чтобы окно не теряло фокус в процессе запуска подпроцессов
startupinfo = None
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

@logger.log
def initHardware(self):
    #Подрубаем общий мониторинг на всю сессию
    computer = Computer()
    #Включаем сбор информации по процу
    computer.IsCpuEnabled = True 
    computer.Open()

    logger.truncateHardwareDumpFile(self)

    return computer

@logger.log
def closeHardware(self):
    self.computer.Close()

@logger.log
def getCpuName(self):
    #Идем по сенсорам и забираем название проца
    for hardware in self.computer.Hardware:
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

@logger.log
def getCoresAndThreadsCount(self):
    data = {
            'status' : Entities.Status.not_collect,
            'cores_count' : 0,
            'threads_count' : 0
           }

    #Идем по сенсорам
    for hardware in self.computer.Hardware:
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

@logger.log
def collectFastData(self, data_lists, cpu_threads):
    data = {
            'status' : Entities.Status.not_collect,
            'all_load' : 0,
            'cpu' : 
                    {
                    'threads' : [],
                    }
           }

    all_load = 0

    for hardware in self.computer.Hardware:
        hardware.Update()

        for sensor in hardware.Sensors:

            #Добавляем загрузку в рамках логических ядер проца
            if str(sensor.SensorType) == 'Load' and 'CPU Core' in str(sensor.Name):
                sensors = str(sensor.Name).split('#')

                #костыль для Intel
                #у него наименование потоков идет так: 
                # "CPU Core #1 Thread #1"
                # "CPU Core #1 Thread #2"
                if len(sensors) == 3:
                    core_number = sensors[1].split(' Thread')[0]
                    core_thread_number = sensors[2]
                    number = str(int(core_number)*2+int(core_thread_number)-2)
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

@logger.log
def collectSlowData(self, data_lists):
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
    for hardware in self.computer.Hardware:
        hardware.Update()

        logger.dumpHardwareToFile(self, '----------sensors---------')

        for sensor in hardware.Sensors:

            sensor_log = f'Type: "{ sensor.SensorType }", Name: "{ sensor.Name }", Value: "{ sensor.Value }"'

            logger.dumpHardwareToFile(self, sensor_log)

            if type(sensor.Value) == NoneType:
                continue
                
            #Добавляем общую температуру проца
            if str(sensor.SensorType) == 'Temperature' and str(sensor.Name) in ('Core (Tctl/Tdie)', 'CPU Package'):
                new_temp = round(sensor.Value, 2)

                old_temp = data_lists['current_temp']

                if old_temp <= 0:
                    data['cpu']['temp'] = new_temp
                else:
                    if new_temp > 0:
                        new_temp = compareAndGetCorrectSensorDataBetweenOldAndNew(new_temp, old_temp)
                    else:
                        new_temp = old_temp

                    data['cpu']['temp'] = new_temp

                continue

            #Добавляем TDP
            if str(sensor.SensorType) == 'Power' and str(sensor.Name) in ('Package', 'CPU Package'):
                new_tdp = round(sensor.Value, 2)

                old_tdp = data_lists['current_TDP']

                if old_tdp <= 0:
                    data['cpu']['tdp'] = new_tdp
                else:
                    if new_tdp > 0:
                        new_tdp = compareAndGetCorrectSensorDataBetweenOldAndNew(new_tdp, old_tdp)
                    else:
                        new_tdp = old_tdp

                    data['cpu']['tdp'] = new_tdp

                continue 

            #Добавляем частоты в рамках физических ядер проца
            if str(sensor.SensorType) == 'Clock' and 'Core' in str(sensor.Name):
                number = str(sensor.Name).split('#')[1]

                value = support.nvl(round(sensor.Value, 2), 0)

                data['cpu']['cores'] += [{'id' : int(number), 'clock' : value }]
                continue 

        logger.dumpHardwareToFile(self, '----------sensors end---------')

    return data

def compareAndGetCorrectSensorDataBetweenOldAndNew(new_data, old_data, smoothing_factor = 1.5, theshold = 3):
    if new_data > old_data*theshold:
        return new_data/smoothing_factor

    if new_data >= 0.1:
        return new_data
    else:
        return old_data

@logger.log
def setCpuPerformanceState(self):
    if not self.config.getIsCPUManagmentOn():
        return

    #Надо проверить, если последние несколько записей были из режима простоя — значит его можно активировать
    #Это надо, чтобы процессор туда-сюда не дергать постоянно
    data = self.data_lists['all_load'][:self.config.getCPUIdleStatePause()]

    idle_ticks_count = len(list(filter(lambda all_load: (all_load < self.config.getCPUThreshhold()), data)))
    turbo_ticks = list(filter(lambda all_load: (all_load >= self.config.getCPUThreshhold()), data[:3]))[::-1]

    if idle_ticks_count == self.config.getCPUIdleStatePause():
        percentage = self.config.getCPUIdleState()
        turbo_id = self.config.getCPUTurboIdleId()
        is_CPU_in_load_mode = False
    else:
        if (len(turbo_ticks) >= 2):
            #Врубаем турбо или если прошло 3 турбо тика или если второй тик больше первого на 15%
            #Так пытаемся минимизировать лишнее включение турбо когда не надо
            if (len(turbo_ticks) >= 3) or (turbo_ticks[1] >= turbo_ticks[0] + 15):
                if int(data[0]) > int(self.config.getCPUThreshhold()):
                    percentage = self.config.getCPULoadState()
                    turbo_id = self.config.getCPUTurboLoadId()
                    is_CPU_in_load_mode = True

                #Во всех других случаях ничего не меняем и возвращаем как есть
                else:
                    is_CPU_in_load_mode = self.config.getIsCPUinLoadMode()
            else:
                is_CPU_in_load_mode = self.config.getIsCPUinLoadMode()
        else:
            is_CPU_in_load_mode = self.config.getIsCPUinLoadMode()

    #Если мы уже в нужном режиме — не переключаем
    if self.config.getIsCPUinLoadMode() == is_CPU_in_load_mode:
        return is_CPU_in_load_mode

    setMaxCPULimits(percentage)

    if self.config.getIsTurboManagmentOn():
        setCPUTurbo(turbo_id)

    #Применим
    applyPowerPlanScheme()

    return is_CPU_in_load_mode

@logger.log
def setCPUtoDefault(self):
    #Проценты
    setMinCPULimits()
    setMaxCPULimits()

    #Турбо
    setCPUTurbo(2)

    #Применим
    applyPowerPlanScheme()

@logger.log
def updateCPUParameters(self, current_config):
    #Получим новые состояния
    new_idle_state = self.config.getCPUIdleState()
    new_load_state = self.config.getCPULoadState()
    new_idle_id = self.config.getCPUTurboIdleId()
    new_load_id = self.config.getCPUTurboLoadId()

    #Получим текущий режим проца
    is_CPU_in_load_mode = current_config.getIsCPUinLoadMode()

    #Проставим минимальные значения состояния процессора
    setMinCPULimits(5, 5)

    #Применим состояния с учетом текущего режима проца, чтобы не включать турбо когда не надо
    if is_CPU_in_load_mode == False:
        setMaxCPULimits(new_idle_state)
        setCPUTurbo(new_idle_id)

    if is_CPU_in_load_mode == True:
        setMaxCPULimits(new_load_state)
        setCPUTurbo(new_load_id)

    #Применим
    applyPowerPlanScheme()

def setMinCPULimits(percentage_ac = 5, percentage_dc = 80):
    subprocess.run('powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN ' + 
                    str(percentage_ac), startupinfo=startupinfo)

    subprocess.run('powercfg -setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN ' + 
                    str(percentage_dc), startupinfo=startupinfo)

def setMaxCPULimits(percentage = 100):
    subprocess.run('powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX ' + 
                    str(percentage), startupinfo=startupinfo)

    subprocess.run('powercfg -setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX ' + 
                    str(percentage), startupinfo=startupinfo)

def setCPUTurbo(id):
    turbo_statuses = Entities.TurboStatuses()
    mode_index = turbo_statuses.getIndexById(id)

    subprocess.run('powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE ' + 
                    mode_index, startupinfo=startupinfo)

    subprocess.run('powercfg -setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE ' + 
                    mode_index, startupinfo=startupinfo)

def applyPowerPlanScheme():
    subprocess.run('powercfg.exe -S SCHEME_CURRENT', startupinfo=startupinfo)

@logger.log
def getAvgTempForSeconds(self, collect_slow_data_interval):
    average_temps_len_perion = len(self.data_lists['average_temps'][:collect_slow_data_interval*self.collect_koef])
    if average_temps_len_perion == 0: return 0

    average_temps_sum_perion = sum(self.data_lists['average_temps'][:collect_slow_data_interval*self.collect_koef])
    avg = average_temps_sum_perion/average_temps_len_perion

    return support.nvl(avg, 0)

@logger.log
def getAvgTDPForSeconds(self, collect_slow_data_interval):
    average_TDPs_len_perion = len(self.data_lists['average_TDP'][:collect_slow_data_interval*self.collect_koef])
    if average_TDPs_len_perion == 0: return 0

    average_TDPs_sum_perion = sum(self.data_lists['average_TDP'][:collect_slow_data_interval*self.collect_koef])
    avg = average_TDPs_sum_perion/average_TDPs_len_perion

    return support.nvl(avg, 0)

def checkSMT(self):
    return self.cpu_cores != self.cpu_threads

if __name__ == "__main__":
    checkSMT()