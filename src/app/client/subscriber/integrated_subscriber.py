import zmq
from threading import Thread
from ...common.indirect_config import DOWNSTREAM_PORT
from .subscriber import Subscriber


class IntegratedSubscriber(Subscriber):
    @property
    def _background_thread(self) -> Thread:
        background_thread = BackgroundThread(self._new_sub_endpoint)
        return Thread(target=background_thread.spin)


class BackgroundThread:
    def __init__(self, new_sub_endpoint: str) -> None:
        self.__new_sub_endpoint = new_sub_endpoint

    def spin(self) -> None:
        receive_new_sub_socket, sub_socket = self.__build_sockets()
        try:
            poller = zmq.Poller()
            poller.register(receive_new_sub_socket, zmq.POLLIN)
            poller.register(sub_socket, zmq.POLLIN)
            while True:
                socks = dict(poller.poll())
                if socks.get(receive_new_sub_socket) == zmq.POLLIN:
                    topic = receive_new_sub_socket.recv_string()
                    sub_socket.setsockopt_string(zmq.SUBSCRIBE, topic)
                if socks.get(sub_socket) == zmq.POLLIN:
                    [topic, msg] = sub_socket.recv_multipart()
                    # TODO: swap for notify callback
                    print(f'{topic}: {msg}')
        except Exception as e:
            if type(e) is not zmq.ContextTerminated:
                print('unexpected exception', e)
        finally:
            receive_new_sub_socket.close()
            sub_socket.close()

    def __build_sockets(self) -> tuple[zmq.Socket, zmq.Socket]:
        receive_new_sub_socket = zmq.Context.instance().socket(zmq.PAIR)
        receive_new_sub_socket.connect(f'inproc://{self.__new_sub_endpoint}')

        sub_socket = zmq.Context.instance().socket(zmq.SUB)
        sub_socket.connect(f'tcp://localhost:{DOWNSTREAM_PORT}')

        return receive_new_sub_socket, sub_socket
