import zmq
from .broker import Broker
from ..common.direct_config import REGISTER_PUB_PORT, REGISTER_SUB_PORT, DISSEMINATE_PUB_PORT
from uuid import uuid4
# TODO: ^^^ drop if not used


class DirectBroker(Broker):
    def __init__(self):
        super().__init__()
        self._context = zmq.Context()
        self._publisher_addresses: list[str] = []
        self._init_register_sub_socket()
        self._init_register_pub_socket()
        self._init_disseminate_pub_socket()
        self._init_poller()
        self._spin()

    def _init_register_sub_socket(self) -> None:
        self._register_subscriber_socket = self._context.socket(zmq.REP)
        self._register_subscriber_socket.bind(f'tcp://*:{REGISTER_SUB_PORT}')

    def _init_register_pub_socket(self) -> None:
        self._register_publisher_socket = self._context.socket(zmq.REP)
        self._register_publisher_socket.bind(f'tcp://*:{REGISTER_PUB_PORT}')

    def _init_disseminate_pub_socket(self) -> None:
        self.disseminate_pub_socket = self._context.socket(zmq.PUB)
        self.disseminate_pub_socket.bind(
            f'tcp://*:{DISSEMINATE_PUB_PORT}'
        )

    def _init_poller(self):
        self._poller = zmq.Poller()
        self._poller.register(self._register_subscriber_socket, zmq.POLLIN)
        self._poller.register(self._register_publisher_socket, zmq.POLLIN)
        # TODO: idk if this needs to be included as POLLOUT, but I'm certain it shouldn't be POLLIN
        # self._poller.register(self.disseminate_pub_socket, zmq.POLLIN)

    def _spin(self) -> None:
        while True:
            socks = dict(self._poller.poll())

            if socks.get(self._register_subscriber_socket) == zmq.POLLIN:
                _ = self._register_subscriber_socket.recv()
                self._register_subscriber_socket.send_string(
                    ','.join(self._publisher_addresses)
                )

            if socks.get(self._register_publisher_socket) == zmq.POLLIN:
                pub_address = self._register_publisher_socket.recv_string()
                self._publisher_addresses.append(pub_address)
                # TODO: generate id and reply with id
                # TODO: hang on ^^^ do we even need the id's for anything?
                # pub_id = uuid4().int
                # self._register_publisher_socket.send_string(pub_id)
                self._register_publisher_socket.send_string('')
                self.disseminate_pub_socket.send_string(pub_address)

            # TODO: pretty sure this one is wrong b/c it doesn't listen, it sends
            # if socks.get(self.disseminate_pub_socket) == zmq.POLLIN:
            #     # TODO: do something
            #     pass

    def __del__(self):
        self._register_subscriber_socket.close()
        self._register_publisher_socket.close()
        self.disseminate_pub_socket.close()
        self._context.term()
