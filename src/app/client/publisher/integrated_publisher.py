import zmq
from ...common.indirect_config import UPSTREAM_PORT
from .publisher import Publisher


class IntegratedPublisher(Publisher):
    def __init__(self, id: str):
        super().__init__(id)
        self.__context = zmq.Context()
        self.__pub_socket = self.__context.socket(zmq.PUB)
        self.__pub_socket.connect(f'tcp://localhost:{UPSTREAM_PORT}')

    def publish(self, topic: str, value: str) -> None:
        self.__pub_socket.send_multipart(
            [bytes(topic, 'ascii'), bytes(value, 'ascii')]
        )

    def __del__(self):
        self.__pub_socket.close()
        self.__context.term()
