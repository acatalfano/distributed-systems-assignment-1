from ...common.broker_mode import BrokerMode
from .publisher import Publisher
from .integrated_publisher import IntegratedPublisher
from .direct_publisher import DirectPublisher


class PublisherFactory:
    def __init__(self, broker_mode: BrokerMode):
        self.broker_mode = broker_mode

    def create(self, id: str) -> Publisher:
        if self.broker_mode == BrokerMode.INDIRECT:
            return IntegratedPublisher(id)
        elif self.broker_mode == BrokerMode.DIRECT:
            return DirectPublisher()
        else:
            raise ValueError
