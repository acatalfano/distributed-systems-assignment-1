import zmq
from .broker import Broker
from ..common.config import UPSTREAM_PORT, DOWNSTREAM_PORT


class IntegratedBroker(Broker):
    def __init__(self):
        super().__init__()
        self.context = zmq.Context()

        self.upstream = self.context.socket(zmq.SUB)
        self.upstream.bind(f'tcp://*:{UPSTREAM_PORT}')
        self.upstream.setsockopt_string(zmq.SUBSCRIBE, '')

        self.downstream = self.context.socket(zmq.PUB)
        self.downstream.bind(f'tcp://*:{DOWNSTREAM_PORT}')

        zmq.device(zmq.FORWARDER, self.downstream, self.upstream)

    def __del__(self):
        self.downstream.close()
        self.upstream.close()
        self.context.term()
