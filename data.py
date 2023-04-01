from math import inf
import copy
import support
import numpy as np

#Функции для сброса записанных данных
def resetGeneralTemps(self):
    self.data_lists['prev_current_temp'] = 0
    self.data_lists['current_temp'] = 0
    self.data_lists['min_temp'] = 0
    self.data_lists['max_temp'] = []

def resetTDP(self):
    self.data_lists['current_TDP'] = 0
    self.data_lists['min_TDP'] = 0
    self.data_lists['max_TDP'] = []

def resetAverage(self):
    self.data_lists['average_temps'] = []
    self.data_lists['average_TDP'] = []

def resetAllData(self):
    self.resetGeneralTemps()
    self.resetTDP()
    self.resetAverage()

    #Записываем данные по температуре
def writeTempData(self, result):        
    #Записываем значения
    cpu_temp = round(result['cpu']['temp'], 1)

    correct_max_temps = copy.copy(self.data_lists['max_temp'])

    if cpu_temp > 0:
        self.data_lists['average_temps'].insert(0, cpu_temp)

        if cpu_temp < self.data_lists['min_temp'] or self.data_lists['min_temp'] == 0:
            self.data_lists['min_temp'] = cpu_temp

        self.data_lists['prev_current_temp'] = self.data_lists['current_temp']
        self.data_lists['current_temp'] = cpu_temp

        correct_max_temps = correct_false_peak_data(self.data_lists['max_temp'], cpu_temp)

    #Обрезаем массивы
    self.data_lists['average_temps'] = self.data_lists['average_temps'][:self.store_period]
    self.data_lists['max_temp'] = correct_max_temps[:self.max_values_cache_ticks]

#Записываем данные по TDP
def writeTDPData(self, result):         
    cpu_TDP = round(result['cpu']['tdp'], 1)

    correct_max_TDPs = copy.copy(self.data_lists['max_TDP'])

    if cpu_TDP > 0 and cpu_TDP != inf:
        self.data_lists['average_TDP'].insert(0, cpu_TDP)

        if (cpu_TDP < self.data_lists['min_TDP']) or self.data_lists['min_TDP'] == 0:
            self.data_lists['min_TDP'] = cpu_TDP

        self.data_lists['current_TDP'] = cpu_TDP

        correct_max_TDPs = correct_false_peak_data(self.data_lists['max_TDP'], cpu_TDP, 1)

    #Обрезаем массивы
    self.data_lists['average_TDP'] = self.data_lists['average_TDP'][:self.store_period]
    self.data_lists['max_TDP'] = correct_max_TDPs[:self.max_values_cache_ticks]

    print(self.data_lists['max_TDP'])

#Записываем данные по ядрам
def writeCoresData(self, result):  
    cores = []   
    for core in result['cpu']['cores']:
        cores.append({'id': int(core['id'])-1, 'clock' : str(core['clock'])})

    self.data_lists['cpu']['cores'] = cores

#Записываем данные по потокам
def writeThreadsData(self, result):
    threads = []

    for thread in result['cpu']['threads']:
        load = support.toRoundStr(thread['load'])
        threads.append({'id': int(thread['id'])-1, 'load' : load})

    self.data_lists['cpu']['threads'] = threads

    if round(result['all_load'], 1) > 0 and result['all_load'] != inf:
        self.data_lists['all_load'].insert(0, result['all_load'])

    self.data_lists['all_load'] = self.data_lists['all_load'][:self.store_period]

def correct_false_peak_data(array, new_value, log = 0):
    #Теперь, чтобы записать данные по макс. температуре и TDP и нам надо исключить явно кривые пики.
    #Для этого мы записываем данные, но те, что отличаются от средних сильно, записываем карандашиком
    #Если потом по среднему значению оказывается, что они правдивы — записываем ручкой.

    tmp_array = copy.copy(array)
    array_len = len(tmp_array)
    correct_coef = 1.25

    #Если массив пустой — вернем как есть
    if array_len == 0:
        return([{ 'value' : new_value, 'type' : 'correct'}])

    #Занесем новое значение с учетом погрешности
    avg_max = np.average([value['value'] for value in tmp_array])
    new_max_temp = None

    if new_value >= avg_max*correct_coef:
        new_max_temp = { 'value' : new_value, 'type' : 'doubtful'}
    elif new_value > tmp_array[0]['value']:
        new_max_temp = { 'value' : new_value, 'type' : 'correct'}

    #Проверим весь массив, возможно для чего-то можно переопределить теперь статус
    corrected_array = []

    for value in tmp_array:
        if value['value'] <= avg_max*correct_coef and value['type'] == 'doubtful':
            corrected_array.append({ 'value' : value['value'], 'type' : 'correct'})
        else:
            corrected_array.append(value)

    #Если новое значение не определили — значит оно и не максимальное, вернем проверенный массив
    if new_max_temp == None:
        return corrected_array

    corrected_array.insert(0, new_max_temp)

    #Если кривое значение только что прилетело и оно одно в массиве — дадим ему шанс и пока оставим как есть
    doubtful_count = len([value for value in corrected_array if value['type'] == 'doubtful'])
    
    if new_max_temp['type'] == 'doubtful' and doubtful_count <= 1:
        return corrected_array

    #Далее, смотрим, если новое значение и предыдущее оба сомнительные и 
    #отличаются не больше чем на 1.25 — окей, запишем
    if new_max_temp['type'] == 'doubtful' and corrected_array[0]['type'] == 'doubtful' \
        and new_max_temp['value'] <= corrected_array[0]['value']*correct_coef:
        return corrected_array

    #Иначе, если все еще не скорректировались — уберем кривые значения, чтобы не копить ошибку
    #А если нет — удалим кривые значения, если они не подряд
    return [value for value in corrected_array if value['type'] == 'correct']