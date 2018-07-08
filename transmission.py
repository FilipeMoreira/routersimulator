class Transmission():

    def __init__(self, _arrivalTime, _startServiceTime, _serviceTime):
        self.arrivalTime = _arrivalTime
        self.startServiceTime = _startServiceTime
        self.serviceTime = _serviceTime
        self.endServiceTime = _startServiceTime + _serviceTime
        self.waitTime = (_startServiceTime - _arrivalTime) or 0

    def log(self):
        print("============================")
        print("Chegada: ", self.arrivalTime)
        print("Começo do serviço: ", self.startServiceTime)
        print("Serviço: ", self.serviceTime)
        print("Tempo de espera: ", self.waitTime)
        print("============================")
# CANAL DE VOZ VAI TER PERIODO DE ATIVIDADE UMA GEOMETRICA COM p = 1/22
# PERIODO DE SILENCIO COMEÇA APENAS 16ms APOS O ULTIMO PACOTE
# PERIODO DE SILENCIO EH UMA EXP(650ms)