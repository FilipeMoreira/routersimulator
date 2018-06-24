import numpy as np
import constants
from eventQueue import EventQueue
from event import Event
from queue import Queue
from packageType import PackageType
from eventType import EventType 
from package import Package

class Simulator:

    def __init__(self, _utilization):
        self.utilization = _utilization

    def simulate(self):
        
        eventQueue = EventQueue()

        pkg = Package(PackageType.DATA_PACKAGE)
        X1 = pkg.size / constants.CHANNEL_SIZE
        print("X1: ", X1)
        print("package size: ", pkg.size)
        print("constants ", X1)
        # arrivalRate = self.utilization / X1
        arrivalRate = 1
        evt = Event(1, np.random.exponential(1/arrivalRate), EventType.CREATE_DATA_PACKAGE)
        eventQueue.add(evt)
        evt = Event(2, constants.VOICE_ARRIVAL_RATE, EventType.CREATE_VOICE_PACKAGE)
        eventQueue.add(evt)

        eventQueue.sort(0, eventQueue.length()-1)
        eventQueue.print()
# PROXIMOS PASSOS:
# ADICIONAR EVENTOS
# ORDENAR A FILA TODA VEZ QUE FOR EXECUTAR UM EVENTO
# RETIRAR ELE DA FILA
# PEGAR O EVENTO E TESTAR A VALIDADE DELE
# POR EXEMPLO, CHEGOU ALGUEM NOVO E O SERVIDOR ESTÁ OCUPADO, TEMOS QUE INTERROMPER CASO NECESSARIO E DISPARAR OUTRO EVENTO
        nextEvent = eventQueue.peek()

            # if(nextEvent.eventType == EventType.CREATE_DATA_PACKAGE):
            #     # do somethinG
            # elif(nextEvent.eventType == EventType.CREATE_VOICE_PACKAGE):
            #     # do somethinG
            # elif(nextEvent.eventType == EventType.DATA_PACKAGE_INTERRUPTED):
            #     # do somethinG
            # elif(nextEvent.eventType == EventType.DATA_PACKAGE_SERVED):
            #     # do somethinG
            # elif(nextEvent.eventType == EventType.VOICE_PACKAGE_SERVED):
            #     # do somethinG
            # elif(nextEvent.eventType == EventType.SILENT_PERIOD):
            #     # do somethinG


    
    def getAverageServiceTime(self, spackageType):
        pass

    def getAverageTotalTime(self, packageType):
        pass

    def getAverageWaitingTime(self, packageType):
        pass

    def getAverageLineLength(self, packageType):
        pass
    
#para 2 Delta Médio e Variância de Delta