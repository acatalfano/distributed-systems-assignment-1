#!/usr/bin/python

from mininet.topo import Topo

from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

# TODO: this was just a copy/paste of a sample from the mininet docs
# N.B: a class that extends Topo can be used as a config with the mininet CLI
#       BUT, the perf_test method (in perf_test.py) is what will let us do automated latency testing stuff
#
# The API has some method for setting up a host to run a command, that's probably what we need


# It took me forever to get mininet installed and to get everything working.
# To run the following sample code use: sudo mn --custom topology.py --topo mytopo --test pingall

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)

topos = { 'mytopo': SingleSwitchTopo }

def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)
    print( "Testing network connectivity" )
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()


# class SingleSwitchTopo(Topo):
#     "Single switch connected to n hosts."
#
#     def build(self, n=2):
#         switch = self.addSwitch('s1')
#         for h in range(n):
#             # Each host gets 50%/n of system CPU
#             host = self.addHost(
#                 'h%s' % (h + 1),
#                 cpu=.5/n
#             )
#             # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
#             self.addLink(
#                 host,
#                 switch,
#                 bw=10,
#                 delay='5ms',
#                 loss=2,
#                 max_queue_size=1000, use_htb=True
#             )
