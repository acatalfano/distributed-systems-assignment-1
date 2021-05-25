import zmq

# Example direct broker from ZMQ docs: https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/forwarder.html

def main():

    context = zmq.Context(1)

    # Socket facing clients
    frontend = context.socket(zmq.SUB)
    frontend.bind("tcp://*:5559")

    frontend.setsockopt_string(zmq.SUBSCRIBE, "")

    # Socket facing services
    backend = context.socket(zmq.PUB)
    backend.bind("tcp://*:5560")

    zmq.device(zmq.FORWARDER, frontend, backend)

if __name__ == "__main__":
    main()