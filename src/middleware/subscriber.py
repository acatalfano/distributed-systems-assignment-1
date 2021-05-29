import zmq


class Subscriber():
    def __init__(self, id: str, port: str):
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(f'tcp://{id}:{port}')

    def subscribe(self, topic: str):
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, bytes(topic, 'ascii'))

    def recv_message(self):
        while True:
            [_, msg] = self.sub_socket.recv_multipart()
            print(f'{msg}')

    def __del__(self):
        self.sub_socket.close()
        self.context.term()
