import zmq
from .direct_publisher import DirectPublisher
from .subscriber import Subscriber
from .broker import Broker


class DirectBroker(Broker):
    # TODO: (I think) this implementation is wrong. the ID's are supposed to be IP address with network port
    def __init__(self):
        self.upstream_port = '5561'
        self.downstream_port = '5562'
        self.context = zmq.Context()
        self.publishers = dict()
        self.subscribers = dict()

    def add_publisher(self, id: str) -> None:
        publisher = DirectPublisher(id, self.downstream_port)
        self.publishers[id] = publisher

    def add_subscriber(self, id: str) -> None:
        subscriber = Subscriber(id, self.downstream_port)
        self.subscribers[id] = subscriber

    def publish(self, id: str, topic: str, value: str) -> None:
        self.publishers[id].publish(topic, value)

    def subscribe(self, id: str, topic: str) -> None:
        self.subscribers[id].subscribe(topic)

    def __del__(self):
        self.subscribers.clear()
        self.publishers.clear()
        self.context.term()
