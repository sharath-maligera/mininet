#!/usr/bin/python

import re
import os
from time import sleep
import json
from mininet.net import Mininet
from mininet.link import TCIntf
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from link import TCLink
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
import iperf3


class StaticTopology(Topo):
    "Simple topo with 2 hosts"

    def __init__(self, init_bw):
        self.init_bw = init_bw
        Topo.__init__(self)

    def build(self):
        switch1 = self.addSwitch('s1')

        "iperf client host"
        host1 = self.addHost('h1', ip='192.168.1.1')
        self.addLink(host1, switch1, bw=self.init_bw)

        "iperf server host"
        host2 = self.addHost('h2', ip='192.168.1.2')
        self.addLink(host2, switch1, bw=self.init_bw)


def plot_bandwidth_limit(traces, plotname, UDP):
    for trace in traces:
        bw_list = []
        for line in open(trace, 'r'):
            if UDP:
                matchObj = re.match(r'(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)', line, re.M)
            else:
                matchObj = re.match(r'(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)', line, re.M)

            if matchObj:
                if UDP:
                    bw = float(matchObj.group(9)) / 8000  # KiloBytes / s
                else:
                    bw = float(matchObj.group(9))   # KiloBytes / s
                bw_list.append(bw)
        plt.plot(bw_list, label='bandwidth')

    plt.legend()
    plt.title("Throughput Comparison")
    plt.ylabel("Throughput [KiloBytes / s]")
    plt.xlabel("Time")
    plt.savefig(plotname)
    #plt.show()

def plot_bandwidth_limit_from_json(server_op_file_name=None, client_op_file_name=None):
    if server_op_file_name is not None:
        with open(server_op_file_name, 'r') as f:
            server_log_dict = json.load(f)


        pass
        print "Completed"


def initialize_iperf(client=None, server=None, server_op_file_name=None, client_op_file_name=None, target_bw=None, UDP=True):
    if None not in (client, server, server_op_file_name, client_op_file_name, target_bw):
        info("Starting iperf Measurement\n")

        # stop old iperf server
        os.system('pkill -f \'iperf -s\'')
        #server.cmd('pkill -f \'iperf -s\'')
        sleep(1)
        # iPerf (iPerf v2) is a tool for active measurements of the maximum achievable bandwidth on IP networks.
        # Initiate iPerf server with -s option
        # -i : Sets the interval time in seconds between periodic bandwidth, jitter, and loss reports.
        #       If non-zero, a report is made every interval seconds of the bandwidth since the last report.
        #       If zero, no periodic reports are printed. Default is zero.
        # -y : Report as a Comma-Separated Values
        # -C : Set the congestion control algorithm
        # > : redirect standard output to file and close the file descriptor with & symbol
        if UDP:
            #server.cmd('iperf3 -s -J > ' + server_op_file_name + ' &')
            # iperf -s -u -l 1248b -f K -w 65k -i 1 -e -t 120 -y C
            server.cmd('iperf -s -u -l 1248b -f K -w 65k -i 1 -e -t 1200 -y C > ' + server_op_file_name + ' &')
        else:
            #server.cmd('iperf3 -s -J > ' + server_op_file_name + ' &')
            server.cmd('iperf3 -s -J > ' + server_op_file_name + ' &')
        sleep(1)

        # Initiate iPerf client with connection to server IP
        # -t : The time in seconds to transmit for. iPerf normally works by repeatedly sending an array of len bytes for time seconds. Default is 10 seconds.
        # -u : Telling iPerf to generate UDP packets
        # -l : The length of UDP data payload in bytes
        if UDP:
            #client.cmd('iperf3 -c ' + str(server.IP()) + ' -u  -f 2.4K -t 100 -i 1 -J > '+ client_op_file_name +' &')
            # iperf -c 192.168.1.108 -u -l 1248b -f K -b 160K -w 64k -t 120 -e --isochronous=1:20K,0 --ipg 5 -y C
            client.cmd('iperf -c ' + str(server.IP()) + ' -u -l 1248b -f K -b 160K -w 64k -t 1200 -e --isochronous=1:20K,0 --ipg 5 -y C &')
        else:
            #client.cmd('iperf3 -c ' + str(server.IP()) + ' -t 100 -i 1 -J > '+ client_op_file_name +' &')
            client.cmd('iperf3 -c ' + str(server.IP()) + ' -t 100 -i 1 -J > ' + client_op_file_name + ' &')
        sleep(1)


def change_bw_limit(client=None, initial_bw=None, target_bw=None, smooth_change=True, interval=None):

    if None not in (client, initial_bw, target_bw, interval):
        client_interface = client.intf()

        info("Setting BW Limit for Interface " + str(client_interface) + " to " + str(target_bw) + "\n")
        # change the bandwidth of link to target bandwidth
        #client_interface.config(bw=target_bw, smooth_change=smooth_change)
        client_interface.config(bw=target_bw, smooth_change=smooth_change)
        sleep(interval)

        # reset bw to initial value
        info("Resetting BW Limit for Interface " + str(client_interface) + " to " + str(0.0192) + "\n")
        client_interface.config(bw=0.0192, smooth_change=smooth_change)
        sleep(interval)

        info("Setting BW Limit for Interface " + str(client_interface) + " to " + str(0.0096) + "\n")
        #client_interface.config(bw=target_bw, smooth_change=smooth_change)
        client_interface.config(bw=0.0096, smooth_change=smooth_change)
        sleep(interval)

        info("Resetting BW Limit for Interface " + str(client_interface) + " to " + str(0.0048) + "\n")
        client_interface.config(bw=0.0048, smooth_change=smooth_change)
        sleep(interval)



def main(initial_bw=None, target_bw=None, change_interval=None, server_op_file_name=None, client_op_file_name=None, plotname=None, UDP=True):
    if None not in (initial_bw, target_bw, change_interval, server_op_file_name, client_op_file_name, plotname):
        topology = StaticTopology(initial_bw)
        #ctl = RemoteController("c1", ip='192.168.1.103', port=6633)
        #net = Mininet(topo=topology, link=TCLink, controller=ctl)
        net = Mininet(topo=topology, link=TCLink)
        net.start()

        print "Testing network connectivity\n"
        net.pingAll()
        print "Dumping host connections\n"
        dumpNodeConnections(net.hosts)
        info("Testing bandwidth between h1 and h2\n")
        h1, h2 = net.getNodeByName('h1', 'h2')
        sleep(5)
        traces = []

        initialize_iperf(client=h1, server=h2, server_op_file_name=server_op_file_name, client_op_file_name=client_op_file_name, target_bw=target_bw, UDP=UDP)
        traces.append(server_op_file_name)
        sleep(change_interval)
        change_bw_limit(client=h1, initial_bw=initial_bw, target_bw=target_bw, interval=change_interval)

        net.stop()
        sleep(5)
        os.system('sudo mn -c')
        plot_bandwidth_limit(traces, plotname, UDP)
        #plot_bandwidth_limit_from_json(server_op_file_name=server_op_file_name, client_op_file_name=server_op_file_name)


if __name__ == '__main__':
    setLogLevel('info')
    target_bandwidth = 0.0384 # 4.8 kBps => 0.0384 Mbit/s   2.4 kBps => 0.0192 Mbit/s   0.6 kBps => 0.0048 Mbit/s
    initial_bandwidth =0.0768 # 9.6 kBps => 0.0768 Mbit/s   1.2 kBps => 0.0096 Mbit/s
    change_interval = 240 # in seconds
    server_op_file_name = 'iperf_server_udp_ipg.log'
    client_op_file_name = 'iperf_client_udp_ipg.json'
    plotname = 'throughput_udp_ipg.png'
    UDP = True
    main(initial_bw=initial_bandwidth, target_bw=target_bandwidth, change_interval=change_interval, server_op_file_name=server_op_file_name, client_op_file_name=client_op_file_name, plotname=plotname, UDP=UDP)