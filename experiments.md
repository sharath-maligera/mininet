# List of experiments conducted

## iPerf2 experiments:
- Experiment to test UDP throughput between hosts.<br/>

![image info](./images/UDP.jpg)

### Server side:
```console
Cvagrant@switch:~$ iperf -s -u -l 1248b -f K -w 64k -i 1
------------------------------------------------------------
Server listening on UDP port 5001
Receiving 1248 byte datagrams
UDP buffer size:  128 KByte (WARNING: requested 64.0 KByte)
------------------------------------------------------------
[  3] local 192.168.1.102 port 5001 connected with 192.168.1.103 port 50083
[ ID] Interval       Transfer     Bandwidth        Jitter   Lost/Total Datagrams
[  3]  0.0- 1.0 sec  19.5 KBytes  19.5 KBytes/sec   0.232 ms    0/   16 (0%)
[  3]  1.0- 2.0 sec  19.5 KBytes  19.5 KBytes/sec   0.263 ms    0/   16 (0%)
[  3]  2.0- 3.0 sec  19.5 KBytes  19.5 KBytes/sec   0.270 ms    0/   16 (0%)
[  3]  3.0- 4.0 sec  19.5 KBytes  19.5 KBytes/sec   0.363 ms    0/   16 (0%)
[  3]  4.0- 5.0 sec  19.5 KBytes  19.5 KBytes/sec   0.303 ms    0/   16 (0%)
[  3]  5.0- 6.0 sec  19.5 KBytes  19.5 KBytes/sec   0.341 ms    0/   16 (0%)
[  3]  6.0- 7.0 sec  19.5 KBytes  19.5 KBytes/sec   0.316 ms    0/   16 (0%)
[  3]  7.0- 8.0 sec  19.5 KBytes  19.5 KBytes/sec   0.276 ms    0/   16 (0%)
[  3]  8.0- 9.0 sec  19.5 KBytes  19.5 KBytes/sec   0.310 ms    0/   16 (0%)
[  3]  9.0-10.0 sec  19.5 KBytes  19.5 KBytes/sec   0.367 ms    0/   16 (0%)
[  3] 10.0-11.0 sec  19.5 KBytes  19.5 KBytes/sec   0.276 ms    0/   16 (0%)
[  3] 11.0-12.0 sec  19.5 KBytes  19.5 KBytes/sec   0.313 ms    0/   16 (0%)
```

``` -l 1248b ``` – denotes 1248 bytes of Datagram.<br/>
``` -f K ``` – report bandwidth in KBytes.<br/>
``` -w 64k ``` – Sets the socket buffer sizes to the specified value. For TCP, this sets the TCP window size. For UDP it is just the buffer which datagrams are received in, and so limits the largest receivable datagram size. Here we are requesting 64KByte but Linux, in it's infinite wisdom, gives us twice what we ask for. Maybe this is to accommodate two way bandwidth testing feature in iPerf2.<br/>
``` -i 1 ``` – Sets the interval time in seconds between periodic bandwidth, jitter, and loss reports.<br/>
