#!/bin/bash

sudo ip tuntap add mode tap eth-A
sudo ifconfig eth-A up

sudo ip tuntap add mode tap eth-B
sudo ifconfig eth-B up

export PATH=$PATH:/usr/share/openvswitch/scripts

ovs-ctl start

ifconfig domainA up
ifconfig domainB up
