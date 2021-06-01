from .topology import SingleSwitchTopo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

# TODO: this was just a copy/paste of a sample from the mininet docs


def perf_test():
    "Create network and run simple performance test"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(
        topo=topo,
        host=CPULimitedHost,
        link=TCLink
    )
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    print("Testing bandwidth between h1 and h4")
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perf_test()
