import zmq
from .broker import Broker


class DirectBroker(Broker):
    def __init__(self):
        super().__init__()

        self.context = zmq.Context()

    # TODO: implement the rest of it -- needs to simply keep track of the pubs/subs and notify

    def __del__(self):
        self.context.term()
