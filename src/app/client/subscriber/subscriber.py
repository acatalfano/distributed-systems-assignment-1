from abc import ABC, abstractmethod


class Subscriber(ABC):
    def __init__(self, id: str = None):
        self.id = id

    @abstractmethod
    def subscribe(self, topic: str) -> None:
        pass
