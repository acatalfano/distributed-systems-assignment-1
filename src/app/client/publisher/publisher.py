import zmq
from ...common.config import UPSTREAM_PORT


class Publisher():
    def __init__(self, id: str):
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.connect(f'tcp://localhost:{UPSTREAM_PORT}')

    def publish(self, topic: str, value: str):
        self.pub_socket.send_multipart(
            [bytes(topic, 'ascii'), bytes(value, 'ascii')]
        )

    def __del__(self):
        self.pub_socket.close()
        self.context.term()
