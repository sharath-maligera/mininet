#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import Host
from functools import partial

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
    topo = SampleTopology()
    privateDirs = [('/var/log', '/tmp/%(name)s/var/log'),
                   ('/var/run', '/tmp/%(name)s/var/run'),
                   '/var/mn']
    host = partial(Host, privateDirs=privateDirs)
    net = Mininet(topo, host=host, link=TCLink, build=False)

    c1 = RemoteController('c1', ip='192.168.1.103', port=6633)
    net.addController(c1)
    net.build()
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    info("Testing bandwidth between h1 and h2\n")
    h1, h2 = net.getNodeByName('h1', 'h2')
    net.iperf((h2, h1), l4Type='UDP')

    p1 = h1.popen('python myServer.py -i %s &' % h1.IP())
    h2.cmd('python myClient.py -i %s -m "hello world"' % h1.IP())

    directories = [directory[0] if isinstance(directory, tuple)
                   else directory for directory in privateDirs]
    #info('Private Directories:', directories, '\n')

    #CLI(net)
    p1.terminate()
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    run_experiment()