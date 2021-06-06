from .subscriber.subscriber import Subscriber
from .publisher.publisher import Publisher
from ..common.broker_mode import BrokerMode
from .subscriber.subscriber_factory import SubscriberFactory
from .publisher.publisher_factory import PublisherFactory


'''
A host can be both a subscriber and publisher
'''


class Host:
    def __init__(self):
        self.subscribers = dict()
        self.publishers = dict()
        self._broker_mode = None

    # TODO: the id's should actually be returned by the broker when adding a sub or pub
    def add_publisher(self, id: str) -> None:
        publisher = self.publisher_factory.create(id)
        self.publishers[id] = publisher

    def add_subscriber(self, id: str) -> None:
        subscriber = self.subscriber_factory.create(id)
        self.subscribers[id] = subscriber

    def publish(self, id: str, topic: str, value) -> None:
        self.get_publisher(id).publish(topic, value)

    def subscribe(self, id: str, topic: str) -> None:
        self.get_subscriber(id).subscribe(topic)

    def get_subscriber(self, id: str) -> Subscriber:
        return self.subscribers[id]

    def get_publisher(self, id: str) -> Publisher:
        return self.publishers[id]

    @property
    def broker_mode(self) -> BrokerMode:
        if self._broker_mode is None:
            # TODO: instead of hardcoded, talk to the broker to get the BrokerMode
            self._broker_mode = BrokerMode.DIRECT
        return self._broker_mode

    @property
    def subscriber_factory(self) -> SubscriberFactory:
        return SubscriberFactory(self.broker_mode)

    @property
    def publisher_factory(self) -> PublisherFactory:
        return PublisherFactory(self.broker_mode)
