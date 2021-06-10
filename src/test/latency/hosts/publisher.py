import click
import random
from threading import Thread
from time import sleep
from app import Host
from .generate_topic_domain import generate_topic_domain


@click.command()
@click.option('-i', '--id', 'host_id', type=str, help="host id")
@click.option(
    '-t',
    '--topic-freq',
    'topic_frequency_pairs',
    type=click.Tuple([str, float]),
    multiple=True,
    help='published topic and frequency pair'
)
@click.option('-n', '--num-t', type=int, help='number of published topics (randomly chosen)')
@click.option('m', '--messages', type=int, help='number of published messages (randomly distributed)')
@click.option('-N', '--total-t', type=int, help='number of globally published topics')
@click.option('-l', '--loop', type=bool, help='whether or not to loop for count mode')
@click.option('-v', '--interval', type=float, default=0.0, help='interval between publishes')
def __main__(host_id: str, topic_frequency_pairs: list[tuple[str, float]], num_t: int, messages: int, total_t: int, interval: float, loop: bool) -> None:
    host = Host()
    host.add_publisher(host_id)

    if topic_frequency_pairs is not None:
        __init_for_topic_frequency_pairs(host_id, host, topic_frequency_pairs)
    elif num_t is not None and total_t is not None and interval is not None and loop is not None and messages is not None:
        if loop:
            while True:
                __init_for_num_and_total(
                    host_id, host, messages, num_t, total_t, interval)
        else:
            __init_for_num_and_total(
                host_id, host, messages, num_t, total_t, interval)


def __init_for_num_and_total(id: str, host: Host, num_t: int, messages: int, total_t: int, interval: float) -> None:
    all_topics = generate_topic_domain(total_t)
    topics = random.sample(all_topics, num_t)
    for message_index in range(messages):
        sleep(interval)
        topic = random.choice(topics)
        host.publish(id, topic, f'{topic} message {message_index}')


def __init_for_topic_frequency_pairs(id: str, host: Host, topic_frequency_pairs: list[tuple[str, float]]) -> None:
    for topic, frequency in topic_frequency_pairs:
        thread = Thread(target=__run_at_frequency,
                        args=(id, host, topic, frequency))
        thread.start()


def __run_at_frequency(id: str, host: Host, topic: str, frequency: float) -> None:
    index: int = 0
    while True:
        sleep(frequency)
        host.publish(id, topic, f'{topic} message {index}')
        index += 1


if __name__ == '__main__':
    __main__()
