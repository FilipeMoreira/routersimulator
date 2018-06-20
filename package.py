import random

class Package():

    #
    #   Classe de pacotes
    #       Tipo Dados: 
    #           Tamanho: 64 - 1500 B
    #              fL(x) = p1*u0(x-64) + p2*u0(x-512) + p3*u0(x-1500) + (p/1436)[u-1(x-64) – u-1(x-1500)]
    #              com p1=30%, p2=10%, p3 = 30%, p = 1 - p1 - p2 - p3 = 30%.
    #

    def __init__(self, _type):
        self.type = _type
        if self.type == 0:
            generateDataPackage()
        elif self.type == 1:
            generateVoicePackage()

    def generateVoicePackage():
        self.size = 512

    def generateDataPackage():
        self.size = int(fL(random.uniform(0,1500)))

    def deltaDeDirac(x,a):
        if x == a:
            return 1
        return 0

    def degrau(x,a):
        if (x-a) >= 0:
            return 1
        return 0

    def fL(x):
        return (0.3*deltaDeDirac(x,64) + 0.1*deltaDeDirac(x,512) + 0.3*deltaDeDirac(x,1500) + ((0.3/1436)*(degrau(x,64)-degrau(x,1500))))