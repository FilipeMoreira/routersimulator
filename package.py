import random
from packageType import PackageType

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
        if self.type == PackageType.DATA_PACKAGE:
            self.size = self.generateDataPackage()
        elif self.type == PackageType.VOICE_PACKAGE:
            self.size = self.generateVoicePackage()

    def generateVoicePackage(self):
        # 512 bits
        return 512

    def generateDataPackage(self):
        # 64 ~ 1500 bytes
        return self.fL(random.uniform(64,1500))

    def deltaDeDirac(self, x, a):
        if x == a:
            return 1
        return 0

    def degrau(self, x ,a):
        if (x-a) >= 0:
            return 1
        return 0

    def fL(self, x):
        packageSizeInBytes = (0.3*self.deltaDeDirac(x,64) + 0.1*self.deltaDeDirac(x,512) + 0.3*self.deltaDeDirac(x,1500) + ((0.3/1436)*(self.degrau(x,64)-self.degrau(x,1500))))
        return packageSizeInBytes * 8