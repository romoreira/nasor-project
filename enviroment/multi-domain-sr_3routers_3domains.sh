#!/bin/bash


sudo ip tuntap add mode tap peeringA-B
sudo ip tuntap add mode tap peeringB-A
sudo ip tuntap add mode tap peeringA-C
sudo ip tuntap add mode tap peeringC-A
sudo ip tuntap add mode tap peeringB-C
sudo ip tuntap add mode tap peeringC-B

sudo ip tuntap add mode tap eth-A
sudo ip tuntap add mode tap eth-B
sudo ip tuntap add mode tap eth-C


sudo ifconfig peeringA-B up
sudo ifconfig peeringB-A up
sudo ifconfig peeringA-C up
sudo ifconfig peeringC-A up
sudo ifconfig peeringB-C up
sudo ifconfig peeringC-B up

sudo ifconfig eth-A up
sudo ifconfig eth-B up
sudo ifconfig eth-C up


sudo ifconfig br-ABBA up
sudo ifconfig br-AC up
sudo ifconfig br-CB up

export PATH=$PATH:/usr/share/openvswitch/scripts

ovs-ctl start

