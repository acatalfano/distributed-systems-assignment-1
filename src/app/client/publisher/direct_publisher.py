import zmq
from .publisher import Publisher
from ...common.direct_config import REGISTER_PUB_PORT, PUBLISHER_PORT, BROKER_IP


class DirectPublisher(Publisher):
    def __init__(self):
        super().__init__()
        self._context = zmq.Context()
        self._init_register_pub_socket()
        self._init_publish_socket()
        self._register_publisher()

    def publish(self, topic: str, value: str) -> None:
        self._publish_socket.send_multipart(
            [bytes(topic, 'ascii'), bytes(value, 'ascii')]
        )

    def _init_register_pub_socket(self):
        self._register_pub_socket = self._context.socket(zmq.REQ)
        self._register_pub_socket.connect(
            f'tcp://{BROKER_IP}:{REGISTER_PUB_PORT}')

    def _init_publish_socket(self):
        self._publish_socket = self._context.socket(zmq.PUB)
        self._publish_socket.bind(f'tcp://*:{PUBLISHER_PORT}')

    def _register_publisher(self):
        # TODO: get the actual ip address...
        ip = 'localhost'
        self._register_pub_socket.send_string(f'{ip}:{PUBLISHER_PORT}')
        self._register_pub_socket.recv()
        self._register_pub_socket.close()

    def __del__(self):
        self._publish_socket.close()
        self._context.term()
