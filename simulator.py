from eventQueue import EventQueue
from event import Event
from queue import Queue

class Simulator:

    def __init__(self, _arrivalRate):
        self.arrivalRate = _arrivalRate

    def simulate(self, usage):

        eventQueue = EventQueue()
        evt = Event(1, 200, 1)
        eventQueue.add(evt)
        evt = Event(2, 340, 1)
        eventQueue.add(evt)
        evt = Event(3, 202, 1)
        eventQueue.add(evt)
        evt = Event(4, 220, 1)
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