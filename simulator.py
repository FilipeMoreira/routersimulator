import numpy as np

from eventQueue import EventQueue
from event import Event
from queue import Queue
from eventType import EventType

class Simulator:

    def __init__(self, _arrivalRate):
        self.arrivalRate = _arrivalRate

    def simulate(self):
        
        eventQueue = EventQueue()
        evt = Event(1, np.random.exponential(1/self.arrivalRate), EventType.CREATE_VOICE_PACKAGE)
        eventQueue.add(evt)
        evt = Event(2, np.random.exponential(1/self.arrivalRate), EventType.CREATE_VOICE_PACKAGE)
        eventQueue.add(evt)
        evt = Event(3, np.random.exponential(1/self.arrivalRate), EventType.CREATE_VOICE_PACKAGE)
        eventQueue.add(evt)
        evt = Event(4, np.random.exponential(1/self.arrivalRate), EventType.CREATE_VOICE_PACKAGE)
        eventQueue.add(evt)

        eventQueue.print()


    def getAverageServiceTime(self, spackageType):
        pass

    def getAverageTotalTime(self, packageType):
        pass

    def getAverageWaitingTime(self, packageType):
        pass

    def getAverageLineLength(self, packageType):
        pass
    
#para 2 Delta Médio e Variância de Delta