import zmq
from .killswitch_listener import KillswitchListener


class Subscriber(KillswitchListener):
    def __init__(self, id: str, port: str, topic: str, killswitch_port: str):
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(f'tcp://{id}:{port}')
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, bytes(topic, 'ascii'))
        KillswitchListener.__init__(
            self,
            self.context,
            killswitch_port,
            self.sub_socket,
            lambda: self.recvMessage()
        )

    def recvMessage(self):
        while True:
            [_, msg] = self.sub_socket.recv_multipart()
            print(f'{msg}')

    def __del__(self):
        self.sub_socket.close()
        self.context.term()
