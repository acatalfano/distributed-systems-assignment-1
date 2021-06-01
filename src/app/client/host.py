from .subscriber.subscriber import Subscriber
from .publisher.publisher import Publisher


'''
A host can be both a subscriber and publisher
'''


class Host:
    def __init__(self):
        self.subscribers = dict()
        self.publishers = dict()

    def add_publisher(self, id: str) -> None:
        publisher = Publisher(id)
        self.publishers[id] = publisher

    def add_subscriber(self, id: str) -> None:
        subscriber = Subscriber(id)
        self.subscribers[id] = subscriber

    def publish(self, id: str, topic: str, value) -> None:
        self.publishers[id].publish(topic, value)

    def subscribe(self, id: str, topic: str) -> None:
        self.subscribers[id].subscribe(topic)
