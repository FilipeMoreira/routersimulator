import numpy as np
import constants
import time
from eventQueue import EventQueue
from event import Event
from queue import Queue
from packageType import PackageType
from eventType import EventType 
from package import Package
from transmission import *


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
        simulationTime = 10000
        simulationLimit = 10000
        arrivalDataRate = self.utilization/0.00302 # = (6040 / 2e+6)
        lastDataPackageTime = 0
        #Transmission(arrivalDataRate,0.14,0.10)
        #exit(-1)

        roundSize = 1000 # packages processed
        transientPhaseSize = 2000 #packages processed
        numberOfRounds = 5
        totalSimulationsPackages = (numberOfRounds * roundSize) + transientPhaseSize

        consumedEvents = []
        eventQueue = EventQueue()
        voiceChannels = []
        voiceQueue = []
        dataQueue = []
        servedPackages = 0

        totalDataWaitingTimePerRound = [0] * numberOfRounds
        totalDataProcessingTimePerRound = [0] * numberOfRounds
        totalVoiceWaitingTimePerRound = [0] * numberOfRounds
        X2PerRound = [0.000256] * numberOfRounds # voice package processing time is fixed due to voice package size being fixed
        # T1 = W1 + X1 | T2 = W2 + X2
        Nq1PerRound = [0] * numberOfRounds
        Nq2PerRound = [0] * numberOfRounds
        voicePackagesProcessedPerRound = [0] * numberOfRounds
        dataPackagesProcessedPerRound = [0] * numberOfRounds


        in_service_package = None

        # Generating voice channels
        for i in range(30):
            voiceChannels.append(VoiceChannel(i))

        currentEvent = None
        currentRound = -1

        while servedPackages < totalSimulationsPackages: #t < simulationTime and len(consumedEvents) < simulationLimit:

            #print('Served packages: ' + str(servedPackages))

            if servedPackages > transientPhaseSize:
                # We're passed transient phase
                currentRound = (servedPackages - transientPhaseSize) % numberOfRounds

            if currentRound >= 0 and (((servedPackages + 1) - transientPhaseSize) % numberOfRounds) > currentRound:
                Nq1PerRound[currentRound] = len(dataQueue)
                Nq2PerRound[currentRound] = len(voiceQueue)

            #print('Simulation time\t' + str(t) + 's\nEvent Queue Size:\t' + str(eventQueue.length()))

            if currentEvent is not None:
                consumedEvents.append(currentEvent)
                #print('Event consumed\t' + str(currentEvent.type))

                # treat evt
                # if the event is a voice package arrival, the package is created and put in the 
                # voice package queue
                if currentEvent.type == EventType.CREATE_VOICE_PACKAGE:
                    voiceQueue.append(Package(PackageType.VOICE_PACKAGE, currentEvent.source, t))
                    #print('Voice Package from ' + constants.PACKAGE_SOURCE[currentEvent.source] + ' queued')
                # if the event type means a voice package should be moved from queue to processing
                # the first package in the queue is removed and we create an event to finish serving it
                elif currentEvent.type == EventType.VOICE_PACKAGE_PROCESSING:
                    in_service_package = voiceQueue.pop(0)
                    in_service_package.startServingTime = t
                    if currentRound >= 0:
                        totalVoiceWaitingTimePerRound[currentRound] += (in_service_package.startServingTime - in_service_package.arrivalTime)
                    eventQueue.add(Event(t + (in_service_package.size/float(constants.CHANNEL_SIZE)), EventType.VOICE_PACKAGE_SERVED, in_service_package.source))
                    #print('Voice Package from ' + constants.PACKAGE_SOURCE[in_service_package.source] + 'is in the router')
                # if the event is a voice package finishing being served we clear the router/server
                elif currentEvent.type == EventType.VOICE_PACKAGE_SERVED:
                    #print('Voice Package from ' + constants.PACKAGE_SOURCE[in_service_package.source] + ' has finished serving')
                    if currentRound >= 0:
                        voicePackagesProcessedPerRound[currentRound] += 1
                    servedPackages += 1
                    in_service_package = None
                # if the event is a data package arrival, the package is created and put in the 
                # data package queue
                elif currentEvent.type == EventType.CREATE_DATA_PACKAGE:
                    dataQueue.append(Package(PackageType.DATA_PACKAGE, currentEvent.source, t))
                    #print('Data Package from ' + constants.PACKAGE_SOURCE[currentEvent.source] + ' with size ' + str(dataQueue[len(dataQueue)-1].size) + ' queued')
                    # here we also create the next data package

                # if the event type means a data package should be moved from queue to processing
                # the first package in the queue is removed and we create an event to finish serving it
                elif currentEvent.type == EventType.DATA_PACKAGE_PROCESSING:
                    in_service_package = dataQueue.pop(0)
                    in_service_package.startServingTime = t
                    if currentRound >= 0:
                        totalDataWaitingTimePerRound[currentRound] += (in_service_package.startServingTime - in_service_package.arrivalTime)
                    eventQueue.add(Event(t + (in_service_package.size/float(constants.CHANNEL_SIZE)), EventType.DATA_PACKAGE_SERVED, in_service_package.source))
                    #print('Data Package from ' + constants.PACKAGE_SOURCE[in_service_package.source] + ' with size ' + str(in_service_package.size) + ' is in the router')
                # if the event is a data package finishing being served we clear the router/server
                elif currentEvent.type == EventType.DATA_PACKAGE_SERVED:
                    #print('Data Package from ' + constants.PACKAGE_SOURCE[in_service_package.source] + ' with size ' + str(in_service_package.size) + ' has finished serving')
                    in_service_package.endServingTime = t
                    if currentRound >= 0:
                        totalDataProcessingTimePerRound[currentRound] += (in_service_package.endServingTime - in_service_package.startServingTime)
                        dataPackagesProcessedPerRound[currentRound] += 1
                    servedPackages += 1
                    in_service_package = None
                # Note: altough voice and data events could be treated together, the separation will make
                # things easier to track and change for the preemptive scenario

            # if there's no package being processed
            if in_service_package is None:
                # we check if there's any voice packages waiting to be processed
                if len(voiceQueue) > 0:
                    eventQueue.add(Event(t, EventType.VOICE_PACKAGE_PROCESSING, voiceQueue[0].source))
                # in case there's no voice package to be processed we check if there's any data package
                # to process
                # Note: this is due to the fact voice packages have the priority
                elif len(dataQueue) > 0:
                    eventQueue.add(Event(t, EventType.DATA_PACKAGE_PROCESSING, 0))


            # Generate voice arrivals
            for i in range(len(voiceChannels)):
                if t >= voiceChannels[i].nextTransmission:
                    evtTimes = voiceChannels[i].getEventTimes(t)[1:]
                    for evtTime in evtTimes:
                        evt = Event(evtTime + t, EventType.CREATE_VOICE_PACKAGE, i+1)
                        #print('Voice evt added in ' + str(evt.eventTime) + 's')
                        eventQueue.add(evt)

            # Generate data arrivals
            evtTime = lastDataPackageTime + np.random.exponential(1/arrivalDataRate)
            eventQueue.add(Event(evtTime, EventType.CREATE_DATA_PACKAGE, 0))
            lastDataPackageTime = evtTime
            #print('Data evt added in ' + str(evtTime) + 's')

            # print('---------')
            # for i in range(eventQueue.length()):
            #     print(str(eventQueue.get(i).type) + ' ' + str(eventQueue.get(i).eventTime))
            # print('---------')

            # getting next event in simulation time and setting simulation time to event's time
            currentEvent = eventQueue.pop()
            # print('--------- next event ---------')
            # print(str(currentEvent.type) + ' ' + str(currentEvent.eventTime))
            # print('---------')
            t = currentEvent.eventTime

        #     package = Package(PackageType.DATA_PACKAGE)
        #     serviceTime = package.size/constants.CHANNEL_SIZE

        #     if(len(self.transmissions) == 0):
        #         # Usando o servico do primeiro cliente para calcular a taxa de chegada
        #         arrivalRate = self.utilization/serviceTime
        #         arrivalTime = np.random.exponential(1/arrivalRate)
        #         serviceStartTime = arrivalTime
        #     else:
        #         arrivalRate = self.utilization/self.average_service_time()
        #         arrivalTime += np.random.exponential(1/arrivalRate)
        #         serviceStartTime = max(arrivalTime, self.transmissions[-1].endServiceTime)
            
        #     # time.sleep(1)
        #     nextTransmission = Transmission(arrivalTime, serviceStartTime, serviceTime)
        #     # nextTransmission.log()
        #     self.transmissions.append(nextTransmission)

        #     t = arrivalTime
        # print("Packages sent ", len(self.transmissions))
        # print("Waiting time ", self.average_wait_time())
        
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

        # GENERATE STATISTICS

        finalW1 = 0
        finalW2 = 0
        finalX1 = 0
        finalX2 = 0
        finalT1 = 0
        finalT2 = 0
        finalNq1 = 0
        finalNq2 = 0

        for i in range(numberOfRounds):
            W1 = totalDataWaitingTimePerRound[i] / dataPackagesProcessedPerRound[i]
            X1 = totalDataProcessingTimePerRound[i] / dataPackagesProcessedPerRound[i]
            T1 = X1 + W1
            W2 = totalVoiceWaitingTimePerRound[i] / voicePackagesProcessedPerRound[i]
            X2 = X2PerRound[i]
            T2 = X2 + W2
            print('Round ' + str(i) + ':\nW1: ' + str(W1) + '\tX1: ' + str(X1) + '\tT1: ' + str(T1))
            print('W2: ' + str(W2) + '\tX2: ' + str(X2) + '\tT2: ' + str(T2) + '\n')

            finalW1 += W1 / numberOfRounds
            finalW2 += W2 / numberOfRounds
            finalX1 += X1 / numberOfRounds
            finalX2 += X2 / numberOfRounds
            finalT1 += T1 / numberOfRounds
            finalT2 += T2 / numberOfRounds
            finalNq1 += dataPackagesProcessedPerRound[i] / numberOfRounds
            finalNq2 += voicePackagesProcessedPerRound[i] / numberOfRounds

        print('E[W1]: ' + str(finalW1))
        print('E[W2]: ' + str(finalW2))
        print('E[X1]: ' + str(finalX1))
        print('E[X2]: ' + str(finalX2))
        print('E[T1]: ' + str(finalT1))
        print('E[T2]: ' + str(finalT2))
        print('E[Nq1]: ' + str(finalNq1))
        print('E[Nq2]: ' + str(finalNq2))

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