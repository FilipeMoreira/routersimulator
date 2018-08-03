#encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import constants
import time
import os
from eventQueue import EventQueue
from event import Event
from queue import Queue
from packageType import PackageType
from eventType import EventType 
from package import Package
from transmission import *
from scipy import stats
import scipy as sp
from numpy import std

class Simulator:

    def __init__(self, _utilization, debug = False, plot = False, preemptive = False):
        self.utilization = _utilization
        self.DEBUG = debug
        self.PLOT = plot
        self.preemptive = preemptive

    def simulate(self):
        t = 0
        simulationTime = 10000
        simulationLimit = 10000
        arrivalDataRate = self.utilization/0.00302 # = (6040 bits / 2e+6 bits/s) s   |   
        lastDataPackageTime = 0

        maxEventListSize = 1000

        roundSize = 2000 # packages processed
        transientPhaseSize = 2500 #packages processed
        numberOfRounds = 10
        totalSimulationsPackages = (numberOfRounds * roundSize) + transientPhaseSize

        consumedEvents = []
        eventQueue = EventQueue()
        voiceChannels = []
        voiceQueue = []
        dataQueue = []
        servedPackages = 0

        totalDataWaitingTimePerRound = [0] * numberOfRounds
        WaitingTimeSamplePerRound = []
        for i in range(numberOfRounds):
            WaitingTimeSamplePerRound.append([])

        totalDataProcessingTimePerRound = [0] * numberOfRounds
        ProcessingTimeSamplePerRound = []
        for i in range(numberOfRounds):
            ProcessingTimeSamplePerRound.append([])

        totalVoiceWaitingTimePerRound = [0] * numberOfRounds
        VoiceWaitingTimeSamplePerRound = []
        for i in range(numberOfRounds):
            VoiceWaitingTimeSamplePerRound.append([])

        X2PerRound = [0.000256] * numberOfRounds # voice package processing time is fixed due to voice package size being fixed
        # T1 = W1 + X1 | T2 = W2 + X2
        Nq1PerRound = [0] * numberOfRounds
        Nq2PerRound = [0] * numberOfRounds

        voicePackagesProcessedPerRound = [0] * numberOfRounds

        dataPackagesProcessedPerRound = [0] * numberOfRounds

        averageVoiceWaitingPerRound = []
        averageDataWaitingPerRound = []
        averageDataServingTimePerRound = []

        transmissions = [{}] * ( constants.VOICE_CHANNELS * numberOfRounds )

        in_service_package = None

        # Generating voice channels
        for i in range(constants.VOICE_CHANNELS):
            voiceChannels.append(VoiceChannel(i))

        currentEvent = None
        currentRound = -1

        servedDataPackages = 0

        while servedDataPackages < totalSimulationsPackages: #t < simulationTime and len(consumedEvents) < simulationLimit:

            # print('Served packages: ' + str(servedPackages))

            if servedDataPackages > transientPhaseSize:
                # We're passed transient phase
                if currentRound != ((servedDataPackages - transientPhaseSize) // roundSize):
                    currentRound = (servedDataPackages - transientPhaseSize) // roundSize
                    #print(currentRound)
                    #print(servedPackages)
                    #print(roundSize)
                    self.log(str(currentRound))


            if currentRound >= 0 and (((servedDataPackages + 1) - transientPhaseSize) // roundSize) > currentRound:
                Nq1PerRound[currentRound] = len(dataQueue)
                Nq2PerRound[currentRound] = len(voiceQueue)

            self.log('Simulation time\t' + str(t) + 's\nEvent Queue Size:\t' + str(eventQueue.length()))

            if currentEvent is not None:
                consumedEvents.append(currentEvent)
                self.log('Event consumed\t' + str(currentEvent.type))

                # treat evt
                # if the event is a voice package arrival, the package is created and put in the 
                # voice package queue
                if currentEvent.type == EventType.CREATE_VOICE_PACKAGE:
                    voiceQueue.append(Package(PackageType.VOICE_PACKAGE, currentEvent.source, t, currentEvent.transmission))
                    self.log('Voice Package from ' + constants.PACKAGE_SOURCE[currentEvent.source] + ' queued')
                # if the event type means a voice package should be moved from queue to processing
                # the first package in the queue is removed and we create an event to finish serving it
                elif currentEvent.type == EventType.VOICE_PACKAGE_PROCESSING:
                    in_service_package = voiceQueue.pop(0)
                    in_service_package.startServingTime = t
                    if currentRound >= 0:
                        totalVoiceWaitingTimePerRound[currentRound] += (in_service_package.startServingTime - in_service_package.arrivalTime)
                        VoiceWaitingTimeSamplePerRound[currentRound].append(in_service_package.startServingTime - in_service_package.arrivalTime)
                        # only for plot purpose
                        averageDataServingTimePerRound.append(sum(totalDataProcessingTimePerRound)/(sum(dataPackagesProcessedPerRound)+1))  
                        averageVoiceWaitingPerRound.append(sum(totalVoiceWaitingTimePerRound)/(sum(voicePackagesProcessedPerRound)+1))
                        averageDataWaitingPerRound.append(sum(totalDataWaitingTimePerRound)/(sum(dataPackagesProcessedPerRound)+1))   

                    eventQueue.add(Event(t + (in_service_package.size/float(constants.CHANNEL_SIZE)), EventType.VOICE_PACKAGE_SERVED, in_service_package.source, in_service_package.transmission))
                    self.log('Voice Package from ' + constants.PACKAGE_SOURCE[in_service_package.source] + 'is in the router')
                # if the event is a voice package finishing being served we clear the router/server
                elif currentEvent.type == EventType.VOICE_PACKAGE_SERVED:
                    self.log('Voice Package from ' + constants.PACKAGE_SOURCE[in_service_package.source] + ' has finished serving')
                    if currentRound >= 0:
                        voicePackagesProcessedPerRound[currentRound] += 1
                    servedPackages += 1

                    if currentRound >= 0 and in_service_package.transmission in transmissions[(in_service_package.source - 1) + (currentRound * constants.VOICE_CHANNELS)].keys():
                        transmission = transmissions[(in_service_package.source - 1) + (currentRound * constants.VOICE_CHANNELS)][in_service_package.transmission]
                        transmission.processedPackages += 1

                        if transmission.size < transmission.processedPackages:
                            transmission.endTime = t
                    
                    in_service_package = None
                # if the event is a data package arrival, the package is created and put in the 
                # data package queue
                elif currentEvent.type == EventType.CREATE_DATA_PACKAGE:
                    dataQueue.append(Package(PackageType.DATA_PACKAGE, currentEvent.source, t, currentEvent.transmission))
                    self.log('Data Package from ' + constants.PACKAGE_SOURCE[currentEvent.source] + ' with size ' + str(dataQueue[len(dataQueue)-1].size) + ' queued')
                    # here we also create the next data package

                # if the event type means a data package should be moved from queue to processing
                # the first package in the queue is removed and we create an event to finish serving it
                elif currentEvent.type == EventType.DATA_PACKAGE_PROCESSING:
                    in_service_package = dataQueue.pop(0)
                    in_service_package.startServingTime = t
                    if currentRound >= 0:
                        totalDataWaitingTimePerRound[currentRound] += (in_service_package.startServingTime - in_service_package.arrivalTime)
                        WaitingTimeSamplePerRound[currentRound].append(in_service_package.startServingTime - in_service_package.arrivalTime)
                        # only for plot purpose
                        averageDataServingTimePerRound.append(sum(totalDataProcessingTimePerRound)/(sum(dataPackagesProcessedPerRound)+1))  
                        averageVoiceWaitingPerRound.append(sum(totalVoiceWaitingTimePerRound)/(sum(voicePackagesProcessedPerRound)+1))
                        averageDataWaitingPerRound.append(sum(totalDataWaitingTimePerRound)/(sum(dataPackagesProcessedPerRound)+1))                    

                    evt = Event(t + (in_service_package.size/float(constants.CHANNEL_SIZE)), EventType.DATA_PACKAGE_SERVED, in_service_package.source, in_service_package.transmission)
                    if self.preemptive:
                        evt.package_reference = in_service_package
                    eventQueue.add(evt)
                    self.log('Data Package from ' + constants.PACKAGE_SOURCE[in_service_package.source] + ' with size ' + str(in_service_package.size) + ' is in the router')
                # if the event is a data package finishing being served we clear the router/server
                elif currentEvent.type == EventType.DATA_PACKAGE_SERVED:
                    self.log('Data Package from ' + constants.PACKAGE_SOURCE[in_service_package.source] + ' with size ' + str(in_service_package.size) + ' has finished serving')
                    in_service_package.endServingTime = t
                    if currentRound >= 0:
                        totalDataProcessingTimePerRound[currentRound] += (in_service_package.endServingTime - in_service_package.startServingTime)
                        dataPackagesProcessedPerRound[currentRound] += 1
                        ProcessingTimeSamplePerRound[currentRound].append(in_service_package.endServingTime - in_service_package.startServingTime)
                        # only for plot purpose
                        averageDataServingTimePerRound.append(sum(totalDataProcessingTimePerRound)/(sum(dataPackagesProcessedPerRound)+1))  
                        averageVoiceWaitingPerRound.append(sum(totalVoiceWaitingTimePerRound)/(sum(voicePackagesProcessedPerRound)+1))
                        averageDataWaitingPerRound.append(sum(totalDataWaitingTimePerRound)/(sum(dataPackagesProcessedPerRound)+1))                        

                      
                    servedPackages += 1
                    servedDataPackages += 1
                    
                    in_service_package = None

                # Note: altough voice and data events could be treated together, the separation will make
                # things easier to track and change for the preemptive scenario

            if self.preemptive:
                if len(voiceQueue) > 0 and in_service_package is not None and in_service_package.type == PackageType.DATA_PACKAGE:
                    totalDataProcessingTimePerRound[currentRound] += (t - in_service_package.startServingTime)
                    ProcessingTimeSamplePerRound[currentRound].append(t - in_service_package.startServingTime)
                    pkg = Package(PackageType.DATA_PACKAGE, 0, t + 0.000256, 0)
                    pkg.size = in_service_package.size # - (( t - in_service_package.startServingTime ) * constants.CHANNEL_SIZE)
                    dataQueue.insert(0, pkg)
                    eventQueue.remove_with_package(in_service_package)
                    in_service_package = None
                    if pkg.size < 0:
                        print("ERROR SIZE")

            # if there's no package being processed
            if in_service_package is None:
                # we check if there's any voice packages waiting to be processed
                if len(voiceQueue) > 0:
                    eventQueue.add(Event(t, EventType.VOICE_PACKAGE_PROCESSING, voiceQueue[0].source, voiceQueue[0].transmission))
                # in case there's no voice package to be processed we check if there's any data package
                # to process
                # Note: this is due to the fact voice packages have the priority
                elif len(dataQueue) > 0:
                    eventQueue.add(Event(t, EventType.DATA_PACKAGE_PROCESSING, 0, 0))


            # Generate voice arrivals
            self.log('==================================')
            for i in range(len(voiceChannels)):
                if t >= voiceChannels[i].nextTransmission:# and eventQueue.length() < maxEventListSize:
                    evtTimes = voiceChannels[i].getEventTimes(t)[1:]
                    transmissionId = 0
                    if currentRound >= 0 and len(evtTimes) > 0:
                        transmission = Transmission(evtTimes[0], 0, (len(evtTimes) - 1), 0)
                        transmissionId = len(transmissions[i + (currentRound * constants.VOICE_CHANNELS)].keys())
                        transmissions[i + (currentRound * constants.VOICE_CHANNELS)][transmissionId] = transmission
                    for evtTime in evtTimes:
                        evt = Event(evtTime + t, EventType.CREATE_VOICE_PACKAGE, i+1, transmissionId)
                        # self.log('Voice evt added in ' + str(evt.eventTime) + 's', 0.005)
                        eventQueue.add(evt)
            self.log('==================================')

            # Generate data arrivals
            if t >= lastDataPackageTime:
                evtTime = lastDataPackageTime + np.random.exponential(1/arrivalDataRate)
                eventQueue.add(Event(evtTime, EventType.CREATE_DATA_PACKAGE, 0, 0))
                lastDataPackageTime = evtTime
                self.log('Data evt added in ' + str(evtTime) + 's')
                #print('Data evt added in ' + str(evtTime) + 's')

            # self.log('---------')
            # for i in range(eventQueue.length()):
            #     self.log(str(eventQueue.get(i).type) + ' ' + str(eventQueue.get(i).eventTime))
            # self.log('---------')

            # getting next event in simulation time and setting simulation time to event's time
            currentEvent = eventQueue.pop()
            # self.log('--------- next event ---------')
            # self.log(str(currentEvent.type) + ' ' + str(currentEvent.eventTime))
            # self.log('---------')
            t = currentEvent.eventTime

        # GENERATE STATISTICS

        finalW1 = 0
        finalStdW1 = 0
        finalW2 = 0
        finalStdW2 = 0
        finalX1 = 0
        finalStdX1 = 0
        finalX2 = 0
        finalStdX2 = 0
        finalT1 = 0
        finalStdT1 = 0
        finalT2 = 0
        finalStdT2 = 0
        finalNq1 = 0
        finalStdNq1 = 0
        finalNq2 = 0
        finalStdNq2 = 0

        delta = 0

        if(self.PLOT):
            if(not(os.path.exists("images"))):
                os.mkdir("images")

            plt.plot(averageDataWaitingPerRound)
            plt.ylabel('E[W1]')
            plt.ylabel('Pacotes servidos')
            plt.title("V.A. W1 com valor rho1 = " + str(self.utilization))
            plt.xlim(xmax = servedPackages)
            plt.savefig('images/W1-'+str(self.utilization)+'.png')
            plt.clf()

            plt.plot(averageDataServingTimePerRound)
            plt.ylabel('E[X1]')
            plt.ylabel('Pacotes servidos')
            plt.title("V.A. X1 com valor rho1 = " + str(self.utilization))
            plt.xlim(xmax = servedPackages)
            plt.savefig('images/X1-'+str(self.utilization)+'.png')
            plt.clf()

            plt.plot(averageVoiceWaitingPerRound)
            plt.ylabel('E[W2]')
            plt.ylabel('Pacotes servidos')
            plt.title("V.A. W2 com valor rho1 = " + str(self.utilization))
            plt.xlim(xmax = servedPackages)
            plt.savefig('images/W2-'+str(self.utilization)+'.png')
            plt.clf()


        stdW1perRound =[]
        stdW2perRound =[]
        stdX1perRound =[]
        stdX2perRound =[]
        stdT1perRound =[]
        stdT2perRound =[]
        stdNq1perRound =[]
        stdNq2perRound =[]

        for i in range(numberOfRounds):
            W1 = totalDataWaitingTimePerRound[i] / dataPackagesProcessedPerRound[i]
            X1 = totalDataProcessingTimePerRound[i] / dataPackagesProcessedPerRound[i]
            T1 = X1 + W1
            stdT1perRound.append(T1)
            W2 = totalVoiceWaitingTimePerRound[i] / voicePackagesProcessedPerRound[i]
            X2 = X2PerRound[i]
            T2 = X2 + W2
            stdT2perRound.append(T2)
            #print('Round ' + str(i) + ':\nW1: ' + str(W1) + '\tX1: ' + str(X1) + '\tT1: ' + str(T1))
            #print('W2: ' + str(W2) + '\tX2: ' + str(X2) + '\tT2: ' + str(T2) + '\n')

            dt = 0
            dt2 = 0
            dts = [0] * constants.VOICE_CHANNELS
            for j in range(len(transmissions) // constants.VOICE_CHANNELS):
                for k in transmissions[j + (i * constants.VOICE_CHANNELS)].keys():
                    transmission = transmissions[j + (i * constants.VOICE_CHANNELS)].get(k)
                    if transmission.endTime > 0:
                        dt += ((transmission.endTime - transmission.startTime) / (len(transmissions[j + (i * constants.VOICE_CHANNELS)]) - 1))
                dts[j] = dt

            for j in range(len(transmissions) // constants.VOICE_CHANNELS):
                for k in transmissions[j + (i * constants.VOICE_CHANNELS)].keys():
                    transmission = transmissions[j + (i * constants.VOICE_CHANNELS)].get(k)
                    if transmission.endTime > 0:
                        dt2 += (((transmission.endTime - transmission.startTime) - dts[j]) ** 2 ) / (len(transmissions[j + (i * constants.VOICE_CHANNELS)]) - 1)


            finalW1 += W1 / numberOfRounds
            stdW1perRound.append(std(WaitingTimeSamplePerRound[i]))

            finalW2 += W2 / numberOfRounds
            stdW2perRound.append(std(VoiceWaitingTimeSamplePerRound[i]))

            finalX1 += X1 / numberOfRounds
            stdX1perRound.append(std(ProcessingTimeSamplePerRound[i]))

            finalX2 += X2 / numberOfRounds

            finalT1 += T1 / numberOfRounds

            finalT2 += T2 / numberOfRounds
            finalNq1 += dataPackagesProcessedPerRound[i] / numberOfRounds            
            finalNq2 += voicePackagesProcessedPerRound[i] / numberOfRounds
            dt /= (constants.M1 * numberOfRounds)
            dt2 /= (constants.M2/(constants.M3 * self.utilization) * numberOfRounds)

        

        finalNq1 = arrivalDataRate * finalW1
        finalNq2 = constants.VOICE_PACKAGE_ARRIVAL_RATE * finalW2
        

        finalStdW1 = std(stdW1perRound)
        finalStdW2 = std(stdW2perRound)
        finalStdX1 = std(stdX1perRound)
        finalStdX2 = std(X2PerRound)

        finalStdNq1 = std(dataPackagesProcessedPerRound)
        finalStdNq2 = std(voicePackagesProcessedPerRound)
        
        finalStdT1 = std(stdT1perRound)
        
        finalStdT2 = std(stdT2perRound)

        print('E[W1]: ' + str(finalW1))
        print('Std[W1]: ' + str(finalStdW1))
        print('IC para W1: ' + str(stats.norm.interval(0.9,loc=finalW1,scale=finalStdW1)))
        print('E[W2]: ' + str(finalW2))
        print('Std[W2]: ' + str(finalStdW2))
        print('IC para W2: ' + str(stats.norm.interval(0.9,loc=finalW2,scale=finalStdW2)))
        print('E[X1]: ' + str(finalX1))
        print('Std[X1]: ' + str(finalStdX1))
        print('IC para X1: ' + str(stats.norm.interval(0.9,loc=finalX1,scale=finalStdX1)))
        print('E[X2]: ' + str(finalX2))
        print('Std[X2]: ' + str(finalStdX2))
        print('IC para X2: ' + str(stats.norm.interval(0.9,loc=finalX2,scale=finalStdX2)))
        print('E[T1]: ' + str(finalT1))
        print('Std[T1]: ' + str(finalStdT1))
        print('IC para T1: ' + str(stats.norm.interval(0.9,loc=finalT1,scale=finalStdT1)))
        print('E[T2]: ' + str(finalT2))
        print('Std[T2]: ' + str(finalStdT2))
        print('IC para T2: ' + str(stats.norm.interval(0.9,loc=finalT2,scale=finalStdT2)))
        print('E[Nq1]: ' + str(finalNq1))
        print('Std[Nq1]: ' + str(finalStdNq1))
        print('IC para Nq1: ' + str(stats.norm.interval(0.9,loc=finalNq1,scale=finalStdNq1)))
        print('E[Nq2]: ' + str(finalNq2))
        print('Std[Nq2]: ' + str(finalStdNq2))
        print('IC para Nq2: ' + str(stats.norm.interval(0.9,loc=finalNq2,scale=finalStdNq2)))
        print('E[Delta]: ' + str(dt))
        print('V[Delta]: ' + str(dt2))

        #print(str(finalT1) + ',' + str(finalW1) + ',' + str(finalX1) + ',' + str(finalNq1) + ',' + str(finalT2) + ',' + str(finalW2) + ',' + str(finalX2) + ',' + str(finalNq2) + ',' + str(dt) + ',' + str(dt2))

    def log(self, message, delay=0.5):
        if(self.DEBUG):
            time.sleep(delay)
            print(message)
    