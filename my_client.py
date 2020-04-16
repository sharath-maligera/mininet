import socket, optparse
from mininet.log import setLogLevel, info

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

print "The ip address of client is "+ str(options.ip)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(options.msg, (options.ip, options.port))