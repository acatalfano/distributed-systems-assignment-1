import zmq
from typing import List


class KillswitchActivator:
    def __init__(self, context: zmq.Context, killswitch_port: str, main_sockets: List[zmq.Socket]) -> None:
        pass

    # TODO: the interrupt logic to make the killswitch port actually do something
    # e.g. a try wrapping the nominal execution case, followed by an "except KeyboardInterrupt : break"
