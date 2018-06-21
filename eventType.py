from enum import Enum

class EventType(Enum):
    # Eventos Possiveis
    # 0 - Criação de pacote de dados
    # 1 - Criação de pacote de voz
    # 2 - Pacote de dados é interrompido
    # 3 - Pacote de dados é servido
    # 4 - Pacote de voz é servido
    # 5 - Período de silêncio (650ms)
    CREATE_DATA_PACKAGE = 0
    CREATE_VOICE_PACKAGE = 1
    DATA_PACKAGE_INTERRUPTED = 2
    DATA_PACKAGE_SERVED = 3
    VOICE_PACKAGE_SERVED = 4
    SILENT_PERIOD = 5
    