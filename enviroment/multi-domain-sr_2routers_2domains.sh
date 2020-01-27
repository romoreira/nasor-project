#!/bin/bash


#Peering Router A Interface
sudo ip tuntap add mode tap peeringA
sudo ifconfig peeringA up

#Internal Router A Interface
sudo ip tuntap add mode tap eth-A-A
sudo ifconfig eth-A-A up


#Peering Router B Interface
sudo ip tuntap add mode tap peeringB
sudo ifconfig peeringB up

#Internal Router B Interface
sudo ip tuntap add mode tap eth-B-B
sudo ifconfig eth-B-B up


sudo ip tuntap add mode tap eth-A
sudo ifconfig eth-A up


sudo ip tuntap add mode tap eth-B
sudo ifconfig eth-B up

export PATH=$PATH:/usr/share/openvswitch/scripts

ovs-ctl start

ifconfig peering up
ifconfig domainA up
ifconfig domainB up
