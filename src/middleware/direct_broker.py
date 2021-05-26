import zmq
from .direct_publisher import DirectPublisher
from .subscriber import Subscriber


class DirectBroker:

    def __init__(self):
        self.upstream_port = '5561'
        self.killswitch_port = '5563'
        self.downstream_port = '5562'
        self.context = zmq.Context()
        self.publishers = dict()
        self.subscribers = []

    def add_publisher(self, id: str):
        publisher = DirectPublisher(self.downstream_port, self.killswitch_port)
        self.publishers[id] = publisher

    def add_subscriber(self, id: str, topic: str):
        subscriber = Subscriber(id, self.downstream_port,
                                topic, self.killswitch_port)
        self.subscribers.append(subscriber)

    def publish(self, id: str, topic: str, value: str):
        self.publishers[id].publish(topic, value)

    def __del__(self):
        self.subscribers.clear()
        self.publishers.clear()
        self.context.term()
