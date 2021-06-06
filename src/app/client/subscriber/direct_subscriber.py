import zmq
from .subscriber import Subscriber
from ...common.direct_config import DISSEMINATE_PUB_PORT, REGISTER_SUB_PORT, BROKER_IP, PUBLISHER_PORT


# TODO: are the IP addresses right? is broker supposed to bind to "localhost" or "*" ?

class DirectSubscriber(Subscriber):
    def __init__(self):
        super().__init__()
        self._context = zmq.Context()
        self._init_disseminate_pub_socket()
        self._init_register_sub_socket()
        self._subscription_sockets: list[zmq.Socket] = []
        self._register_subscriber()

    def subscribe(self, topic: str) -> None:
        for socket in self._subscription_sockets:
            socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    def _init_disseminate_pub_socket(self):
        self._disseminate_pub_socket = self._context.socket(zmq.SUB)
        self._disseminate_pub_socket.connect(
            f'tcp://{BROKER_IP}:{DISSEMINATE_PUB_PORT}')

    def _init_register_sub_socket(self):
        self._register_sub_socket = self._context.socket(zmq.REQ)
        self._register_sub_socket.connect(
            f'tcp://{BROKER_IP}:{REGISTER_SUB_PORT}')

    def _register_subscriber(self):
        self._register_sub_socket.send(b'')
        addresses_str: str = self._register_sub_socket.recv_string()
        pub_addresses = filter(
            lambda address: len(address) > 0,
            addresses_str.split(',')
        )
        for address in pub_addresses:
            sub_socket = self._context.socket(zmq.SUB)
            sub_socket.connect(f'tcp://{address}')
            # sub_socket.connect(f'tcp://{address}:{PUBLISHER_PORT}')
            self._subscription_sockets.append(sub_socket)
        self._register_sub_socket.close()
        # self._spin()

    def _spin(self) -> None:
        poller = zmq.Poller()
        poller.register(self._disseminate_pub_socket, zmq.POLLIN)
        for sub in self._subscription_sockets:
            poller.register(sub, zmq.POLLIN)
        while True:
            socks = dict(poller.poll())
            if socks.get(self._disseminate_pub_socket) == zmq.POLLIN:
                self._add_subscription()

            for sub in self._subscription_sockets:
                if socks.get(sub) == zmq.POLLIN:
                    _, message = sub.recv_multipart()
                    print(message)
                    # TODO: notify client of the message somehow

    def _add_subscription(self):
        new_address = self._disseminate_pub_socket.recv_string()
        new_subscription = self._context.socket(zmq.SUB)
        new_subscription.connect(f'tcp://{new_address}')
        print(f'connected to socket at tcp://{new_address}')
        # new_subscription.connect(
        #     f'tcp://{new_address}:{PUBLISHER_PORT}')
        self._subscription_sockets.append(new_subscription)

    def __del__(self):
        self._disseminate_pub_socket.close()
        for socket in self._subscription_sockets:
            socket.close()
        self._context.term()
