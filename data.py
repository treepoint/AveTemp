from math import inf
import support

#Функции для сброса записанных данных
def resetGeneralTemps(self):
    self.data_lists['general_temps'] = []
    self.data_lists['current_temp'] = 0
    self.data_lists['prev_current_temp'] = 0
    self.data_lists['min_temp'] = 0
    self.data_lists['max_temp'] = 0

def resetTDP(self):
    self.data_lists['general_TDP'] = []
    self.data_lists['current_TDP'] = 0
    self.data_lists['min_TDP'] = 0
    self.data_lists['max_TDP'] = 0

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

    if cpu_temp > 0:
        self.data_lists['general_temps'].insert(0, result['cpu']['temp'])
        self.data_lists['average_temps'].insert(0, result['cpu']['temp'])

        if cpu_temp < self.data_lists['min_temp'] or self.data_lists['min_temp'] == 0:
            self.data_lists['min_temp'] = cpu_temp

        if cpu_temp > self.data_lists['max_temp']:
            self.data_lists['max_temp'] = cpu_temp

        self.data_lists['prev_current_temp'] = self.data_lists['current_temp']
        self.data_lists['current_temp'] = cpu_temp
    
    #Обрезаем массивы
    self.data_lists['general_temps'] = self.data_lists['general_temps'][:self.store_period]
    self.data_lists['average_temps'] = self.data_lists['average_temps'][:self.store_period]

#Записываем данные по TDP
def writeTDPData(self, result):         
    cpu_TDP = round(result['cpu']['tdp'], 1)

    if cpu_TDP > 0 and cpu_TDP != inf:
        self.data_lists['general_TDP'].insert(0, result['cpu']['tdp'])
        self.data_lists['average_TDP'].insert(0, result['cpu']['tdp'])

        if (cpu_TDP < self.data_lists['min_TDP']) or self.data_lists['min_TDP'] == 0:
            self.data_lists['min_TDP'] = cpu_TDP

        if cpu_TDP > self.data_lists['max_TDP']:
            self.data_lists['max_TDP'] = cpu_TDP

        self.data_lists['current_TDP'] = cpu_TDP

    #Обрезаем массив
    self.data_lists['general_TDP'] = self.data_lists['general_TDP'][:self.store_period]
    self.data_lists['average_TDP'] = self.data_lists['average_TDP'][:self.store_period]

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