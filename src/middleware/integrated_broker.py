import zmq
from .publisher import Publisher
from .subscriber import Subscriber
from .killswitch_activator import KillswitchActivator


class IntegratedBroker(KillswitchActivator):
    def __init__(self):
        self.upstream_port = '5561'
        self.downstream_port = '5562'
        self.killswitch_port = '5563'
        self.context = zmq.Context()

        self.upstream = self.context.socket(zmq.XSUB)
        self.upstream.bind(f'tcp://*:{self.upstream_port}')

        self.downstream = self.context.socket(zmq.XPUB)
        self.downstream.bind(f'tcp://*:{self.downstream_port}')

        KillswitchActivator.__init__(
            self,
            self.context,
            self.killswitch_port,
            [self.upstream, self.downstream]
        )

        self.publishers = dict()
        self.subscribers = []

    # TODO: vvvv this probably should be moved into a class under "public"

    def add_publisher(self, id: str):
        publisher = Publisher(id, self.downstream_port, self.killswitch_port)
        self.publishers[id] = publisher

    def add_subscriber(self, id: str, topic: str):
        subscriber = Subscriber(
            id,
            self.downstream_port,
            topic,
            self.killswitch_port
        )
        self.subscribers.append(subscriber)

    def publish(self, id: str, topic: str, value: str):
        self.publishers[id].publish(topic, value)

    def __del__(self):
        self.subscribers.clear()
        self.publishers.clear()
        self.context.term()
