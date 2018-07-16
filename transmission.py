#encoding: utf-8
from package import Package
from packageType import PackageType
import numpy as np
import constants

class Transmission():

    def __init__(self, _startTime, _endTime, _size, _processedPackages):
        self.startTime = _startTime
        self.endTime = _endTime
        self.size = _size
        self.processedPackages = _processedPackages

    def log(self):
        print("============================")
        print("Chegada: ", self.arrivalTime)
        print("Começo do serviço: ", self.startServiceTime)
        print("Serviço: ", self.serviceTime)
        print("Tempo de espera: ", self.waitTime)
        print("============================")

    # def voice_channel(self):
    #     self.voice_queue = [Package(PackageType.VOICE_PACKAGE) for i in range(30)]

class VoiceChannel():
    def __init__(self, ident):
        self.id = ident
        self.nextTransmission = 0
        
    def getEventTimes(self, initialTime):
        self.silent_period = np.random.exponential(1/0.65)
        self.package_num = np.random.geometric(1/22)
        self.service_time = self.package_num * constants.VOICE_ARRIVAL_RATE

        self.services_start_time = []
        self.services_start_time.append(0)
        for i in range(self.package_num - 1):
            self.services_start_time.append(self.services_start_time[-1] + constants.VOICE_ARRIVAL_RATE)     
        #print(self.services_start_time)
        self.nextTransmission = initialTime + self.services_start_time[-1] + self.silent_period + constants.VOICE_ARRIVAL_RATE
        #print('Next Voice transmission: ' + str(self.nextTransmission) + 's')
        return self.services_start_time    

    def average_data(self):
        i = 0
        silent_period_sum = 0
        package_num_sum = 0
        max = 10000
        while i < max:
            silent_period_sum +=  np.random.exponential(0.65)
            package_num_sum += np.random.geometric(1/22)
            i+=1
        print("silent average: ", silent_period_sum/max)
        print("package average: ", package_num_sum/max)
# CANAL DE VOZ VAI TER PERIODO DE ATIVIDADE UMA GEOMETRICA COM p = 1/22
# PERIODO DE SILENCIO COMEÇA APENAS 16ms APOS O ULTIMO PACOTE
# PERIODO DE SILENCIO EH UMA EXP(650ms)