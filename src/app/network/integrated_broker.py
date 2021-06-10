import zmq
from .broker import Broker
from ..common.indirect_config import UPSTREAM_PORT, DOWNSTREAM_PORT


class IntegratedBroker(Broker):
    # When creating a new integrated broker we set our upstream and down stream ports to the configured ports
    def __init__(self):
        super().__init__()
        self.context = zmq.Context()

        self.upstream = self.context.socket(zmq.XSUB)
        self.upstream.bind(f'tcp://*:{UPSTREAM_PORT}')

        self.downstream = self.context.socket(zmq.XPUB)
        self.downstream.bind(f'tcp://*:{DOWNSTREAM_PORT}')
        self.__start()

    def __del__(self):
        self.downstream.close()
        self.upstream.close()
        self.context.term()

    def __start(self):
        try:
            zmq.proxy(self.upstream, self.downstream)
        except Exception as e:
            self.__del__()
