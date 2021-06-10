#!/usr/bin/python
from typing import Callable
import click
from mininet.topo import Topo
from mininet.node import CPULimitedHost, Host
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class SingleSwitchTopo(Topo):
    def build(self, n_subs: int, n_pubs: int):
        self.broker: str = 'hb1'
        self.pubs: list[str] = []
        self.subs: list[str] = []

        sub_to_broker_switch = self.addSwitch('s1')
        pub_to_broker_switch = self.addSwitch('s2')

        n_hosts = 1 + n_pubs + n_subs

        broker = self.addHost(self.broker, cpu=.5/n_hosts)
        self.__add_link(broker, sub_to_broker_switch)
        self.__add_link(broker, pub_to_broker_switch)

        for s in range(n_subs):
            sub_name = f'hs{s}'
            self.subs.append(sub_name)
            sub = self.addHost(sub_name, cpu=.5/n_hosts)
            self.__add_link(sub, sub_to_broker_switch)

        for p in range(n_pubs):
            pub_name = f'hp{p}'
            self.pubs.append(pub_name)
            pub = self.addHost(pub_name, cpu=.5/n_hosts)
            self.__add_link(pub, pub_to_broker_switch)

    def __add_link(self, h1: str, h2: str) -> None:
        self.addLink(
            h1,
            h2,
            bw=10,
            delay='5ms',
            loss=2,
            max_queue_size=1000,
            usb_htb=True
        )


@click.group(chain=True, invoke_without_command=True)
@click.option('-s', '--sub-count', type=int, help='number of subscribers')
@click.option('-p', '--pub-count', type=int, help='number of publishers')
@click.option('-N', '--total-topics', 'num_topics', type=int, help='number of topics in system (for count-mode)')
def latency_test(sub_count: int, pub_count: int, num_topics: int):
    pass


@latency_test.result_callback()
def callback(processors: list[Callable[[Mininet, int], Mininet]], sub_count: int, pub_count: int, num_topics: int) -> None:
    topo = SingleSwitchTopo(sub_count, pub_count)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    broker: Host = net.get(topo.broker)
    broker.cmd('python3.9 ./hosts/broker.py')
    
    for proc in processors:
        net = proc(net, num_topics)
    net.start()


@latency_test.command('sub')
@click.option('-i', '--id', 'host_id', type=str, help='host id')
@click.option('-n', '--num-t', type=int, help='number of subscribed topics (randomly chosen)')
@click.option('-v', '--interval', type=float, default=0.0, help='interval between subscriptions')
@click.option('-w', '--wait-time', type=float, default=0.0, help='spin time in the callback')
@click.option(
    '-t',
    '--topic_delay',
    'topic_delay_pairs',
    type=click.Tuple([str, int]),
    multiple=True,
    help='pair of subscribed topic and delay from previous subscription'
)
def sub_command(host_id: str, topic_delay_pairs: list[tuple[str, int]], wait_time: float, num_t: int, interval: float) -> Callable[[Mininet, int], Mininet]:
    def processor(net: Mininet, total_topics: int) -> tuple[Mininet, int]:
        if host_id is not None and wait_time is not None and topic_delay_pairs is not None:
            __init_subs_by_topics(net, host_id, wait_time, topic_delay_pairs)
        elif host_id is not None and num_t is not None and wait_time is not None and interval is not None:
            __init_subs_by_counts(net, total_topics, host_id,
                                  num_t, wait_time, interval)
        return net

    return processor


@latency_test.command('pub')
@click.option('-i', '--id', 'host_id', type=str, help="host id")
@click.option(
    '-t',
    '--topic-freq',
    'topic_frequency_pairs',
    type=click.Tuple([str, float]),
    multiple=True,
    help='published topic and frequency pair'
)
@click.option('-m', '--messages', type=int, help='number of published messages (randomly distributed)')
@click.option('-n', '--num-t', type=int, help='number of published topics (randomly chosen)')
@click.option('-l', '--loop', type=bool, help='whether or not to loop for count mode')
@click.option('-v', '--interval', type=float, default=0.0, help='interval between publishes')
def pub_command(host_id: str, messages: int, topic_frequency_pairs: list[tuple[str, float]], num_t: int, interval: float, loop: bool) -> Callable[[Mininet, int], Mininet]:
    def processor(net: Mininet, total_topics: int) -> tuple[Mininet, int]:
        if host_id is not None and topic_frequency_pairs is not None:
            __init_pubs_by_topics(net, host_id, topic_frequency_pairs)
        elif host_id is not None and num_t is not None and interval is not None and loop is not None:
            __init_pubs_by_counts(net, total_topics, host_id,
                                  num_t, interval, messages, loop)
        return net

    return processor


def __init_subs_by_topics(net: Mininet, host_id: str, wait_time: float, sub_topics: list[tuple[str, int]]) -> None:
    topic_args: str = ' '.join(
        [f'-t {topic} {delay}' for topic, delay in sub_topics])
    cmd: str = f'python3.9 ./hosts/subscriber.py -i {host_id} {topic_args} -w {wait_time}'
    sub: Host = net.get(f'hs{host_id}')
    sub.cmdPrint(cmd)


def __init_subs_by_counts(net: Mininet, total_topics: int, host_id: str, num_topics: float, wait_time: float, interval: float) -> None:
    cmd: str = f'python3.9 ./hosts/subscriber.py -i {host_id} -w {wait_time} -n {num_topics} -N {total_topics} -v {interval}'
    sub: Host = net.get(f'hs{host_id}')
    sub.cmdPrint(cmd)


def __init_pubs_by_topics(net: Mininet, host_id: str, topic_frequency_pairs: list[tuple[str, float]]) -> None:
    topic_args: str = ' '.join(
        [f'-t {topic} {freq}' for topic, freq in topic_frequency_pairs])
    cmd: str = f'python3.9 ./hosts/publisher.py -i {host_id} {topic_args}'
    pub: Host = net.get(f'hp{host_id}')
    pub.cmdPrint(cmd)


def __init_pubs_by_counts(net: Mininet, total_topics: int, host_id: str, num_topics: float, interval: float, messages: int, loop: bool) -> None:
    cmd: str = f'python3.9 ./hosts/publisher.py -i {host_id} -n {num_topics} -N {total_topics} -v {interval} -m {messages} -l {loop}'
    pub: Host = net.get(f'hp{host_id}')
    pub.cmdPrint(cmd)


if __name__ == '__main__':
    setLogLevel('info')
    latency_test()
