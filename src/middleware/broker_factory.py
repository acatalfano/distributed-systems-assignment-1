from .broker import Broker
from .integrated_broker import IntegratedBroker
from .direct_broker import DirectBroker
from .broker_config import BROKER_MODE, BrokerMode


class BrokerFactory:
    @staticmethod
    def build_broker() -> Broker:
        if BROKER_MODE == BrokerMode.DIRECT:
            return DirectBroker()
        elif BROKER_MODE == BrokerMode.INDIRECT:
            return IntegratedBroker()
        else:
            raise ValueError(BROKER_MODE)
