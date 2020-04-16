#!/usr/bin/python

import re
import os
from time import sleep

from mininet.net import Mininet
from mininet.link import TCIntf
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from link import TCLink
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mininet.node import RemoteController

TARGET_BW = 0.0048
INITIAL_BW = 0.0096


class StaticTopo(Topo):
    "Simple topo with 2 hosts"

    def build(self):
        switch1 = self.addSwitch('s1')

        "iperf client host"
        host1 = self.addHost('h1', ip='192.168.1.1')
        self.addLink(host1, switch1, bw=INITIAL_BW)

        "iperf server host"
        host2 = self.addHost('h2', ip='192.168.1.2')
        self.addLink(host2, switch1, bw=INITIAL_BW)


def plotIperf(traces):
    for trace in traces:
        bw_list = []
        for line in open(trace[0], 'r'):
            matchObj = re.match(r'(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)', line, re.M)

            if matchObj:
                bw = float(matchObj.group(9)) / 1000.0 / 1000.0   # MBit / s
                bw_list.append(bw)
        plt.plot(bw_list, label=trace[1])

    plt.legend()
    plt.title("Throughput Comparison")
    plt.ylabel("Throughput [KiloBit / s]")
    plt.xlabel("Time")
    plt.savefig('throughput_4.png')
    #plt.show()


def measureChange(client=None, server=None, smooth_change=False, output_file_name=None, target_bw=TARGET_BW):
    info("Starting iperf Measurement\n")

    # stop old iperf server
    os.system('pkill -f \'iperf -s\'')
    #server.cmd('pkill -f \'iperf -s\'')
    sleep(1)

    # Initiate iPerf server with -s option
    # -i : Sets the interval time in seconds between periodic bandwidth, jitter, and loss reports.
    #       If non-zero, a report is made every interval seconds of the bandwidth since the last report.
    #       If zero, no periodic reports are printed. Default is zero.
    # -y : Report as a Comma-Separated Values
    # -C : Set the congestion control algorithm
    # > : redirect standard output to file and close the file descriptor with & symbol
    server.cmd('iperf -s -i 0.5 -y C > ' + output_file_name + ' &')
    sleep(1)

    # Initiate iPerf client with connection to server IP
    # -t : The time in seconds to transmit for. iPerf normally works by repeatedly sending an array of len bytes for time seconds. Default is 10 seconds.
    # -u : Telling iPerf to generate UDP packets
    # -l : The length of UDP data payload in bytes
    client.cmd('iperf -c ' + str(server.IP()) + ' -t 10 -i 1 > /dev/null &')

    # wait 10 seconds before changing
    sleep(10)

    intf = client.intf()
    info("Setting BW Limit for Interface " + str(intf) + " to " + str(target_bw) + "\n")
    # change the bandwidth of link to target bandwidth
    intf.config(bw=target_bw, smooth_change=smooth_change)

    # wait a few seconds to finish
    sleep(10)


def limit():
    myTopo = StaticTopo()
    ctl = RemoteController("c1", ip='192.168.1.103', port=6633)
    net = Mininet(topo=myTopo, link=TCLink, controller=ctl)
    net.start()

    print "Testing network connectivity"
    net.pingAll()
    info("Testing bandwidth between h1 and h2\n")
    h1, h2 = net.getNodeByName('h1', 'h2')
    sleep(5)
    traces = []

    filename = 'iperfServer_hard_4.log'
    measureChange(client=h1, server=h2, smooth_change=False, output_file_name=filename)
    traces.append((filename, 'Hard'))
    #
    # reset bw to initial value
    intf = h2.intf()
    intf.config(bw=INITIAL_BW)
    #sleep(5)

    filename = 'iperfServer_smooth_4.log'
    measureChange(client=h1, server=h2, smooth_change=True, output_file_name=filename)
    traces.append((filename, 'Smooth'))
    #
    # # reset bw to initial value
    # intf.config(bw=INITIAL_BW)
    #
    # filename = 'iperfServer_nolimit.log'
    # #measureChange(h1, h2, False, filename, target_bw=None)
    # #traces.append((filename, 'No limit'))
    #
    net.stop()

    plotIperf(traces)


if __name__ == '__main__':
    setLogLevel('info')
    limit()