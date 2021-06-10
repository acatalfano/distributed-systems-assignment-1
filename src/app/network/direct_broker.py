import zmq
from .broker import Broker
from ..common.direct_config import REGISTER_PUB_PORT, REGISTER_SUB_PORT, DISSEMINATE_PUB_PORT
from uuid import uuid4
# TODO: ^^^ drop if not used


class DirectBroker(Broker):
    def __init__(self):
        super().__init__()
        self.__context = zmq.Context()
        self.__publisher_addresses: list[str] = []
        self.__init_register_sub_socket()
        self.__init_register_pub_socket()
        self.__init_disseminate_pub_socket()
        self.__init_poller()
        self.__spin()

    def __init_register_sub_socket(self) -> None:
        self._register_subscriber_socket = self.__context.socket(zmq.REP)
        self._register_subscriber_socket.bind(f'tcp://*:{REGISTER_SUB_PORT}')

    def __init_register_pub_socket(self) -> None:
        self._register_publisher_socket = self.__context.socket(zmq.REP)
        self._register_publisher_socket.bind(f'tcp://*:{REGISTER_PUB_PORT}')

    def __init_disseminate_pub_socket(self) -> None:
        self.disseminate_pub_socket = self.__context.socket(zmq.PUB)
        self.disseminate_pub_socket.bind(
            f'tcp://*:{DISSEMINATE_PUB_PORT}'
        )

    def __init_poller(self):
        self._poller = zmq.Poller()
        self._poller.register(self._register_subscriber_socket, zmq.POLLIN)
        self._poller.register(self._register_publisher_socket, zmq.POLLIN)

    def __spin(self) -> None:
        while True:
            socks = dict(self._poller.poll())

            if socks.get(self._register_subscriber_socket) == zmq.POLLIN:
                _ = self._register_subscriber_socket.recv()
                self._register_subscriber_socket.send_string(
                    ','.join(self.__publisher_addresses)
                )

            if socks.get(self._register_publisher_socket) == zmq.POLLIN:
                pub_address = self._register_publisher_socket.recv_string()
                self.__publisher_addresses.append(pub_address)
                self._register_publisher_socket.send_string('')
                self.disseminate_pub_socket.send_string(pub_address)

    def __del__(self):
        self._register_subscriber_socket.close()
        self._register_publisher_socket.close()
        self.disseminate_pub_socket.close()
        self.__context.term()
