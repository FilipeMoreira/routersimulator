#encoding: utf-8

class Event:

    # Eventos Possiveis
    # 0 - Criação de pacote de dados
    # 1 - Criação de pacote de voz
    # 2 - Pacote de dados é interrompido
    # 3 - Pacote de dados é servido
    # 4 - Pacote de voz é servido
    # 5 - Período de silêncio (650ms)

    def __init__(self, _eventTime, _type, _source, _transmission):
        self.eventTime = _eventTime
        self.type = _type
        self.source = _source
        self.transmission = _transmission
        self.package_reference = 0
