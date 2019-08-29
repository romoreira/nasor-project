#!/bin/bash
echo "Setting enviroment variables to OvS"
sudo source ~/.bashrc
echo "Setting up OvS"
sudo ovs-ctl start
echo "Creating OvS Bridge (br-int)"
sudo ovs-vsctl add-br br-int
echo "Configuring Bridge Address (to reach SDN controller)"
sudo ifconfig br-int 10.0.0.10 netmask 255.255.255.0 up
echo "Creating Network Interfaces (vnet)"
sudo ip tuntap add mode tap vnet0
sudo ip tuntap add mode tap vnet1
sudo ip tuntap add mode tap vnet2
echo "Setting up Network Interfaces (vnet)"
sudo ifconfig vnet0 up
sudo ifconfig vnet1 up
sudo ifconfig vnet2 up
echo "Adding vnets to OvS"
sudo ovs-vsctl add-port br-int vnet0
sudo ovs-vsctl add-port br-int vnet1
sudo ovs-vsctl add-port br-int3 vnet2
echo "Done"
