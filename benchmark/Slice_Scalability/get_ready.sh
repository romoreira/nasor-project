#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
sudo apt-get -y --force-yes install ethtool
sudo apt-get -y --force-yes install iperf
sudo apt-get -y --force-yes install iperf3
sudo apt-get -y --force-yes install libpcap-dev

git clone https://github.com/the-tcpdump-group/tcpdump
cd tcpdump/
sudo ./configure
sudo make && sudo make install && cd ..

sudo sysctl -w net.ipv6.conf.all.forwarding=1

cd SRv6-net-prog/srext/
sudo make && sudo make install && depmod -a

sudo modprobe srext

exit