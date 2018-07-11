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
    DATA_PACKAGE_PROCESSING = 2
    VOICE_PACKAGE_PROCESSING = 3
    DATA_PACKAGE_INTERRUPTED = 4
    DATA_PACKAGE_SERVED = 5
    VOICE_PACKAGE_SERVED = 6
    SILENT_PERIOD = 7
    