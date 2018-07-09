import numpy as np
import constants
import time
from eventQueue import EventQueue
from event import Event
from queue import Queue
from packageType import PackageType
from eventType import EventType 
from package import Package
from transmission import Transmission


class Simulator:

    def __init__(self, _utilization):
        self.utilization = _utilization
        self.transmissions = []

    def simulate(self):
        
        # eventQueue = EventQueue()

        # USANDO A UTILIZAÇÃO NO COMEÇO APENAS PARA DISPARAR A SIMULAÇÃO 
        # evt = Event(np.random.exponential(1/self.utilization), EventType.CREATE_DATA_PACKAGE)
        # eventQueue.add(evt)
        t = 0
        simulationTime = 100
        Transmission(0.1,0.14,0.10)
        exit(-1)
        while t < simulationTime:
            package = Package(PackageType.DATA_PACKAGE)
            serviceTime = package.size/constants.CHANNEL_SIZE

            if(len(self.transmissions) == 0):
                # Usando o servico do primeiro cliente para calcular a taxa de chegada
                arrivalRate = self.utilization/serviceTime
                arrivalTime = np.random.exponential(1/arrivalRate)
                serviceStartTime = arrivalTime
            else:
                arrivalRate = self.utilization/self.average_service_time()
                arrivalTime += np.random.exponential(1/arrivalRate)
                serviceStartTime = max(arrivalTime, self.transmissions[-1].endServiceTime)
            
            # time.sleep(1)
            nextTransmission = Transmission(arrivalTime, serviceStartTime, serviceTime)
            # nextTransmission.log()
            self.transmissions.append(nextTransmission)

            t = arrivalTime
        print("Packages sent ", len(self.transmissions))
        print("Waiting time ", self.average_wait_time())
        
        ################
        # MMIQ EXAMPLE #
        ################
        ##calculate arrival date and service time for new customer
		# if len(Customers)==0:
		# 	arrival_date=neg_exp(lambd)
		# 	service_start_date=arrival_date
		# else:
		# 	arrival_date+=neg_exp(lambd)
		# 	service_start_date=max(arrival_date,Customers[-1].service_end_date)
		# service_time=neg_exp(mu)
		##create new customer
		# Customers.append(Customer(arrival_date,service_start_date,service_time))
		# #increment clock till next end of service
		# t=arrival_date

    def average_service_time(self):
        if(len(self.transmissions) > 0):
            serviceTimeSum = 0
            for t in self.transmissions:
                serviceTimeSum += t.serviceTime
            return serviceTimeSum/len(self.transmissions)
        return 0

    def getAverageServiceTime(self, spackageType):
        pass

    def getAverageTotalTime(self, packageType):
        pass

    def average_wait_time(self):
        if(len(self.transmissions) > 0):
            waitingSum = 0
            for t in self.transmissions:
                waitingSum += t.waitTime
            return waitingSum/len(self.transmissions)
        return 0

    def getAverageLineLength(self, packageType):
        pass
    
#para 2 Delta Médio e Variância de Delta