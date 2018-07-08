class Transmission():

    def __init__(self, _arrivalTime, _startServiceTime, _serviceTime):
        self.arrivalTime = _arrivalTime
        self.startServiceTime = _startServiceTime
        self.serviceTime = _serviceTime
        self.endServiceTime = _serviceTime + _startServiceTime
        self.waitTime = _startServiceTime - _arrivalTime


