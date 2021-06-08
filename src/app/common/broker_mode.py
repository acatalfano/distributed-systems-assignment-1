from enum import Enum


class BrokerMode(Enum):
    DIRECT = 1
    INDIRECT = 2


BROKER_MODE: BrokerMode = BrokerMode.DIRECT
