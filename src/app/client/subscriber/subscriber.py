import zmq
from ...common.config import DOWNSTREAM_PORT


class Subscriber():
    def __init__(self, id: str):
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect(f'tcp://localhost:{DOWNSTREAM_PORT}')
        self.spin = True
        # TODO: currently only works if you only do all you "subscribe(topic)" calls before "recv_message()"
        #           ideally, you should be able to add subscriptions after "recv_message()" is spinning
        #           ...not a zmq limitation, it's b/c as-is, it's a single thread that blocks on an infinite loop
        #           probably want to do something with an extra socket (plus zmq.Poller) or threading manually
        # self.recv_message()

    def subscribe(self, topic: str):
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, bytes(topic, 'ascii'))

    def recv_message(self):
        # TODO: remove all these print()'s when done w/ that level of sanity-debugging
        print('receiving messages')
        # TODO: something other than infinite loop (kill signal from broker? -- or is it okay to be simple for now?)
        while self.spin:
            [_, msg] = self.sub_socket.recv_multipart()
            print(f'{msg}')

    def __del__(self):
        self.spin = False
        self.sub_socket.close()
        self.context.term()
