import zmq
from .broker import Broker
from ..common.config import UPSTREAM_PORT, DOWNSTREAM_PORT


class IntegratedBroker(Broker):
    def __init__(self):
        super().__init__()
        self.context = zmq.Context()

        self.upstream = self.context.socket(zmq.XSUB)
        self.upstream.bind(f'tcp://*:{UPSTREAM_PORT}')

        self.downstream = self.context.socket(zmq.XPUB)
        self.downstream.bind(f'tcp://*:{DOWNSTREAM_PORT}')
        zmq.proxy(self.upstream, self.downstream)

    def __del__(self):
        self.downstream.close()
        self.upstream.close()
        self.context.term()
