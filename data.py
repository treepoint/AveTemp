from math import inf
import copy
import support

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

        correct_max_TDPs = correct_false_peak_data(self.data_lists['max_TDP'], cpu_TDP)

    #Обрезаем массивы
    self.data_lists['average_TDP'] = self.data_lists['average_TDP'][:self.store_period]
    self.data_lists['max_TDP'] = correct_max_TDPs[:self.max_values_cache_ticks]

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

def correct_false_peak_data(array, new_value):
    #Теперь, чтобы записать данные по макс. температуре и TDP и нам надо исключить явно кривые пики.
    #Для этого мы записываем данные, но те, что отличаются от средних сильно, записываем карандашиком
    #Если потом по среднему значению оказывается, что они правдивы — записываем ручкой.

    result_array = []

    #Посчитаем кол-во значений и среднее макс значение
    array_len = len(array)
    avg_max = 0

    if array_len != 0:
        for max_temp in array:
            avg_max += max_temp['value']
    
        avg_max = avg_max/array_len

    #Занесем новое значение с учетом погрешности
    if array_len == 0 or new_value > avg_max:
        new_max_temp = { 'value' : new_value, 'type' : 'correct'}

        if new_value >= (avg_max)*1.25 and avg_max != 0:
            new_max_temp['type'] = 'doubtful'

        array.insert(0, new_max_temp)

    #Проверим весь массив, возможно для чего-то можно переопределить теперь статус
    max_array = []

    for value in array:
        updated_max_value = value

        if updated_max_value['value'] <= (avg_max)*1.25:
            updated_max_value['type'] = 'correct'
        
        max_array.append(value)

    #Если кривое значение только что прилетело — дадим ему шанс и пока оставим как есть
    #Но только если их не два суммарно в массиве, чтобы не копить ошибку
    doubtful_count = len([value for value in max_array if value['type'] == 'doubtful'])

    if max_array[0]['type'] == 'doubtful' and doubtful_count <= 1:
        return max_array

    #А теперь удалим кривые значения, если они не подряд
    prev_value = None

    is_sequence_of_doubtful = False
    for value in max_array:
        if prev_value == None:
            prev_value = value
            continue
        
        if value['type'] == prev_value['type']:
            is_sequence_of_doubtful = True
            break

    #Если последовательности нет — удалим сомнительные
    if not is_sequence_of_doubtful:
        result_array = [value for value in max_array if value['type'] == 'correct']
    else:
        result_array = max_array

    #Вернем скорректированный массив
    return result_array