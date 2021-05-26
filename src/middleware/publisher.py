import zmq
from .killswitch_listener import KillswitchListener


class Publisher(KillswitchListener):
    def __init__(self, id: str, port: str, killswitch_port: str):
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.connect(f'tcp://{id}:{port}')
        KillswitchListener.__init__(
            self,
            self.context,
            killswitch_port,
            self.pub_socket,
            lambda: None
        )

    def publish(self, topic: str, value: str):
        self.pub_socket.send_multipart(
            [bytes(topic, 'ascii'), bytes(value, 'ascii')]
        )

    def __del__(self):
        self.pub_socket.close()
        self.context.term()
