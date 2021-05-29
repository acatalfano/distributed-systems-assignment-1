class ClientSub:
    def __init__(self):
        # TODO: setup ports and context
        raise NotImplementedError()

    def register_sub(self, topic: str, id: str) -> None:
        # TODO: REQ/REP to register w/ broker on the well-known address/port
        raise NotImplementedError()

    def notify(self, topic: str, value) -> None:
        # TODO: push-based notify-method (this gets called every time the broker publishes to this client-sub)
        raise NotImplementedError()

    def __del__(self):
        # TODO: cleanup the ports and context
        raise NotImplementedError()
