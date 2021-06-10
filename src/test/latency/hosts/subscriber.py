import random
import click
from time import sleep
from app import Host
from .generate_topic_domain import generate_topic_domain


@click.command()
@click.option('-i', '--id', 'host_id', type=str, help='host id')
@click.option(
    '-t',
    '--topic_delay',
    'topic_delay_pairs',
    type=click.Tuple([str, int]),
    multiple=True,
    help='pair of subscribed topic and delay from previous subscription'
)
@click.option('-n', '--num-t', type=int, help='number of published topics (randomly chosen)')
@click.option('-N', '--total-t', type=int, help='number of globally published topics')
@click.option('-v', '--interval', type=float, default=0.0, help='interval between subscriptions')
@click.option('-w', '--wait-time', type=float, default=0.0, help='spin time in the callback')
def __main__(host_id: str, topic_delay_pairs: list[tuple[str, int]], wait_time: float, num_t: int, total_t: int, interval: float) -> None:

    def callback(topic: str, message: str) -> None:
        print(
            f'''
            received topic: {topic}
            with message: {message}
            '''
        )
        sleep(wait_time)

    host = Host(callback)
    host.add_subscriber(host_id)

    if topic_delay_pairs is not None:
        __init_for_topic_delay_pairs(host_id, host, topic_delay_pairs)
    elif num_t is not None and total_t is not None and interval is not None:
        __init_for_num_and_total(host_id, host, num_t, total_t, interval)
    # TODO: add click to requirements.txt


def __init_for_topic_delay_pairs(id: str, host: Host, topic_delay_pairs: list[tuple[str, int]]) -> None:
    for topic, delay in topic_delay_pairs:
        sleep(delay)
        host.subscribe(id, topic)


def __init_for_num_and_total(id: str, host: Host, num_t: int, total_t: int, interval: float) -> None:
    all_topics = generate_topic_domain(total_t)
    topics = random.sample(all_topics, num_t)
    for t in topics:
        sleep(interval)
        host.subscribe(id, t)


if __name__ == '__main__':
    __main__()
