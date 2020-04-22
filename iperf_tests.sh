#!/bin/bash

################################
# Jimmy Cullen                 #
# Version 1.0, 2011-05-04      #
# The University of Manchester #
################################

# Revision 1.1, 2011-06-02
# iperf-2.0.2 used with the -r flag causes incorrect output, therefore removed from script

# Script to test bi-directional UDP bandwidth between two hosts using iperf.
# Loop through bandwidth values 100M - 10G and datagram sizes 1000 - 8972 bytes.
# Data output is in csv format to file.

# NB - passwordless login (e.g. ssh keys) must setup between hosts for the script to work.

my_name=`uname -n`
machine_A_ip="192.168.10.206"
machine_A_name="gig1.hep.manchester.ac.uk"
machine_A_user="jimmy"
machine_B_ip="192.168.10.100"
machine_B_name="jb10g"
machine_B_user="jnc"

date=`date +%F_%R`
server_filename="\$HOME/iperf_test_server_$date.txt"
client_filename="$HOME/iperf_test_client_$date.txt"
pkt_size_array=(1000 1472 2000 3000 4000 5000 6000 7000 8000 8972)

if [ "$my_name" = "$machine_A_name" ]; then

	# machine_A is the client

	for b in ${pkt_size_array[*]}; do
		echo "Entering loop with packet size = $b bytes"
		for a in `seq 1 100`; do
                	s_cmd="\$HOME/iperf-2.0.2/src/iperf -u -s -w 256k -l "$b"B -f m"
                	echo "Running command on server"
                	ssh -f $machine_B_user@$machine_B_ip "touch $server_filename; echo $s_cmd >> $server_filename; $s_cmd >> $server_filename"

			echo "Entering loop with bandwidth = $(($a*100)) Mbps"
			c_cmd="$HOME/iperf-2.0.2/src/iperf -u -c $machine_B_ip -b $(($a*100))M -w 256K -l "$b"B -y C -f m"
			echo $c_cmd >> $client_filename
			sleep 3
			echo "Running client command"
			$c_cmd >> $client_filename
                	sleep 2
		done
	done

else

	# machine_B is the client

	for b in ${pkt_size_array[*]}; do
		echo "Entering loop with packet size = $b bytes"
		for a in `seq 1 100`; do
			s_cmd="\$HOME/iperf-2.0.2/src/iperf -u -s -w 256k -l "$b"B -f m"
                        echo "Running command on server"
			ssh -f $machine_A_user@$machine_A_ip "touch $server_filename; echo $s_cmd >> $server_filename; $s_cmd >> $server_filename"

			echo "Entering loop with bandwidth = $(($a*100)) Mbps"
			c_cmd="$HOME/iperf-2.0.2/src/iperf -u -c $machine_A_ip -b $(($a*100))M -w 256K -l "$b"B -y C -f m"
			echo $c_cmd >> $client_filename
			sleep 3
			echo "Running client command"
                        $c_cmd >> $client_filename
                        sleep 2
		done
	done

fi