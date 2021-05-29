class ClientPub:
    def __init__(self):
        # TODO: setup context and ports
        raise NotImplementedError()

    def register_pub(self, topic: str, id: str) -> None:
        # TODO: register via REQ/REP with the broker at the well-known address/port
        raise NotImplementedError()

    def publish(self, topic: str, value) -> None:
        # TODO: publish a topic to the broker
        raise NotImplementedError()

    def __del__(self):
        # TODO: cleanup the ports and context
        raise NotImplementedError()
