#!/usr/bin/python

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg, info
import socket

def main():
    lg.setLogLevel('info')

    net = Mininet(SingleSwitchTopo(k=2))
    net.start()

    h1 = net.get('h1')
    print "The ip address of client is " + str(h1.IP())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto("hello world", (options.ip, options.port))


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print "Server IP address is " + str(h1.IP())
    server_socket.bind((h1.IP(), 12345))



    f = open('foo.txt', 'w')
    while True:
        data, addr = server_socket.recvfrom(512)
        f.write("%s: %s\n" % (addr, data))
        f.flush()



    p1 = h1.popen('python my_server.py -i %s &' % h1.IP())

    h2 = net.get('h2')
    h2.cmd('python my_client.py -i %s -m "hello world"' % h1.IP())

    #CLI( net )
    p1.terminate()
    net.stop()

if __name__ == '__main__':
    main()