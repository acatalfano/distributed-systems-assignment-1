from typing import NoReturn
import zmq
from collections.abc import Callable


class KillswitchListener:
    def __init__(
        self,
        context: zmq.Context,
        killswitch_port: str,
        main_socket: zmq.Socket,
        main_socket_callback
            # main_socket_callback: Callable[[], None] = lambda: None
            # TODO: struggling with typing on this one
    ) -> None:
        self.killswitch_socket = context.socket(zmq.SUB)
        self.killswitch_socket.bind(f'tcp://*:{killswitch_port}')
        self.killswitch_socket.setsockopt(zmq.SUBSCRIBE, b'')
        self.main_socket = main_socket
        self.main_socket_callback = main_socket_callback

    def poll_sockets(self) -> None:
        poller = zmq.Poller()
        poller.register(self.main_socket, zmq.POLLIN)
        poller.register(self.killswitch_socket, zmq.POLLIN)

        while True:
            socks = dict(poller.poll())

            if socks.get(self.main_socket) == zmq.POLLIN:
                self.main_socket_callback()
            if socks.get(self.killswitch_socket) == zmq.POLLIN:
                break

        self.killswitch_socket.close()

    def __del__(self) -> None:
        self.killswitch_socket.close()
