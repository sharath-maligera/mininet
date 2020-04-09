#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.link import TCLink

class SampleTopology( Topo ):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )
        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        s1 = self.addSwitch( 's1' )

        #Add links between hosts and switches
        self.addLink(h1, s1, bw=20, delay='5ms', loss=0)
        self.addLink(h2, s1, bw=10, delay='10ms', loss=10)


def run_experiment():
    "Create and test a simple experiment"
    topo = SampleTopology( )
    net = Mininet(topo, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    info("Testing bandwidth between h1 and h2\n")
    h1, h2 = net.getNodeByName('h1', 'h2')
    net.iperf((h1, h2), l4Type='UDP')
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    run_experiment()