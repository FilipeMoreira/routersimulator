import random
from packageType import PackageType
import numpy as np

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

    def fL(self, x):
        # Escolhe um dos 3 tamanhos, caso não consiga, escolhe um tamanho usando a uniforme
        packageSizeInBytes = np.random.choice([64,512,1500,np.random.uniform(64,1500)], p=[0.3, 0.1, 0.3, 0.3])
        return packageSizeInBytes * 8
     