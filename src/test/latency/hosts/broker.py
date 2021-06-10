from app import BrokerFactory


def __main__() -> None:
    factory = BrokerFactory()
    factory.build_broker()


if __name__ == '__main__':
    __main__()
