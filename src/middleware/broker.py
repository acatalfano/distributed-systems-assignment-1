from abc import ABC, abstractmethod


class Broker(ABC):
    @abstractmethod
    def add_publisher(self, network_identifier: str) -> None:
        pass

    @abstractmethod
    def add_subscriber(self, network_identifier: str) -> None:
        pass

    @abstractmethod
    def publish(self, network_identifier: str, topic: str, value: str) -> None:
        pass

    @abstractmethod
    def subscribe(self, network_identifier: str, topic: str) -> None:
        pass
