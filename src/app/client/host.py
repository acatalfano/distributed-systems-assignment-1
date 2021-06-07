from typing import Callable
from .subscriber.subscriber import Subscriber
from .publisher.publisher import Publisher
from ..common.broker_mode import BrokerMode
from .subscriber.subscriber_factory import SubscriberFactory
from .publisher.publisher_factory import PublisherFactory


'''
A host can be both a subscriber and publisher
'''


class Host:
    def __init__(self, callback: Callable[[str, str], None]):
        self.__callback = callback
        self.__subscribers: dict[str, Subscriber] = dict()
        self.__publishers: dict[str, Publisher] = dict()
        self.__broker_mode_value = None

    # TODO: the id's should actually be returned by the broker when adding a sub or pub
    def add_publisher(self, id: str) -> None:
        publisher = self.__publisher_factory.create(id)
        self.__publishers[id] = publisher

    def add_subscriber(self, id: str) -> None:
        subscriber = self.__subscriber_factory.create(id)
        self.__subscribers[id] = subscriber

    def publish(self, id: str, topic: str, value) -> None:
        self.__publishers[id].publish(topic, value)

    def subscribe(self, id: str, topic: str) -> None:
        self.__subscribers[id].subscribe(topic)

    @property
    def __broker_mode(self) -> BrokerMode:
        if self.__broker_mode_value is None:
            # TODO: instead of hardcoded, talk to the broker to get the BrokerMode
            self.__broker_mode_value = BrokerMode.INDIRECT
        return self.__broker_mode_value

    @property
    def __subscriber_factory(self) -> SubscriberFactory:
        return SubscriberFactory(self.__broker_mode, self.__callback)

    @property
    def __publisher_factory(self) -> PublisherFactory:
        return PublisherFactory(self.__broker_mode)
