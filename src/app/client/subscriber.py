import zmq
from ..common.config import DOWNSTREAM_PORT


class Subscriber():
    # TODO: need this to be tcp://IP_ADDRESS/ID:UPSTREAM_PORT
    def __init__(self, id: str):
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(f'tcp://localhost:{DOWNSTREAM_PORT}')
        self.spin = True
        # self.recv_message()
        # TODO: something other than infinite loop (kill signal from broker? -- or is it okay to be simple for now?)

    def subscribe(self, topic: str):
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, bytes(topic, 'ascii'))

    def recv_message(self):
        print('receiving messages')
        while self.spin:
            [_, msg] = self.sub_socket.recv_multipart()
            print(f'{msg}')

    def __del__(self):
        self.spin = False
        self.sub_socket.close()
        self.context.term()
