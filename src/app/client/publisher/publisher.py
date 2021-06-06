from abc import ABC, abstractmethod


class Publisher(ABC):
    def __init__(self, id: str = None):
        self.__id = id

    @abstractmethod
    def publish(self, topic: str, value: str) -> None:
        pass
