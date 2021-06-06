import zmq
from threading import Thread

from .subscriber import Subscriber
from ...common.direct_config import DISSEMINATE_PUB_PORT, REGISTER_SUB_PORT, BROKER_IP, PUBLISHER_PORT


# TODO: are the IP addresses right? is broker supposed to bind to "localhost" or "*" ?

class DirectSubscriber(Subscriber):
    @property
    def _background_thread(self) -> Thread:
        background_thread = BackgroundThread(self._new_sub_endpoint)
        return Thread(target=background_thread.run_background_thread)


class BackgroundThread:
    def __init__(self, new_sub_endpoint: str):
        self.__new_sub_endpoint = new_sub_endpoint
        self.__subscription_sockets: list[zmq.Socket] = []
        self.__subscribed_topics: list[str] = []

    def run_background_thread(self) -> None:
        try:
            self.__register_subscriber()
            self.__spin()
        except Exception as e:
            if type(e) is not zmq.ContextTerminated:
                print('unexpected exception', e)
        finally:
            for socket in self.__subscription_sockets:
                socket.close()

    def __register_subscriber(self) -> None:
        register_sub_socket = zmq.Context.instance().socket(zmq.REQ)
        try:
            register_sub_socket.connect(
                f'tcp://{BROKER_IP}:{REGISTER_SUB_PORT}')

            register_sub_socket.send(b'')
            addresses_str: str = register_sub_socket.recv_string()
            pub_addresses = filter(
                lambda address: len(address) > 0,
                addresses_str.split(',')
            )
            for address in pub_addresses:
                sub_socket = zmq.Context.instance().socket(zmq.SUB)
                sub_socket.connect(f'tcp://{address}')
                # sub_socket.connect(f'tcp://{address}:{PUBLISHER_PORT}')
                self.__subscription_sockets.append(sub_socket)
        finally:
            register_sub_socket.close()

    def __build_sockets(self) -> None:
        self.__receive_new_sub_socket = zmq.Context.instance().socket(zmq.PAIR)
        self.__receive_new_sub_socket.connect(
            f'inproc://{self.__new_sub_endpoint}')

        self.__disseminate_pub_socket = zmq.Context.instance().socket(zmq.SUB)
        self.__disseminate_pub_socket.connect(
            f'tcp://{BROKER_IP}:{DISSEMINATE_PUB_PORT}')

    def __spin(self) -> None:
        self.__build_sockets()

        poller = zmq.Poller()
        poller.register(self.__receive_new_sub_socket, zmq.POLLIN)
        poller.register(self.__disseminate_pub_socket, zmq.POLLIN)
        for sub in self.__subscription_sockets:
            poller.register(sub, zmq.POLLIN)

        while True:
            socks = dict(poller.poll())
            if socks.get(self.__disseminate_pub_socket) == zmq.POLLIN:
                new_sub_socket = self.__add_sub_connection()
                self.__subscribe_to_all_topics(new_sub_socket)

                # register new socket and store in running list
                poller.register(new_sub_socket, zmq.POLLIN)
                self.__subscription_sockets.append(new_sub_socket)

            if socks.get(self.__receive_new_sub_socket) == zmq.POLLIN:
                topic: str = self.__receive_new_sub_socket.recv_string()
                self.__subscribe_on_all_sockets(topic)
                # add topic to running list
                self.__subscribed_topics.append(topic)

            for sub in self.__subscription_sockets:
                if socks.get(sub) == zmq.POLLIN:
                    topic, message = sub.recv_multipart()
                    # TODO: swap for notify callback
                    print(f'{topic}: {message}')

    def __add_sub_connection(self) -> zmq.Socket:
        new_address = self.__disseminate_pub_socket.recv_string()
        new_subscription = zmq.Context.instance().socket(zmq.SUB)
        new_subscription.connect(f'tcp://{new_address}')
        return new_subscription

    def __subscribe_to_all_topics(self, new_sub_socket: zmq.Socket) -> None:
        for topic in self.__subscribed_topics:
            new_sub_socket.setsockopt_string(zmq.SUBSCRIBE, topic)

    def __subscribe_on_all_sockets(self, topic: str) -> None:
        for socket in self.__subscription_sockets:
            socket.setsockopt_string(zmq.SUBSCRIBE, topic)
