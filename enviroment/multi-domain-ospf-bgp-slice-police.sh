#!/bin/bash


#Creating interfaces in Hosts
sudo ip tuntap add mode tap r1-r2-port
sudo ip link set r1-r2-port up

sudo ip tuntap add mode tap r2-r1-port
sudo ip link set r2-r1-port up


sudo ip tuntap add mode tap r2-r3-port
sudo ip link set r2-r3-port up


sudo ip tuntap add mode tap r3-r2-port
sudo ip link set r3-r2-port up

sudo ip tuntap add mode tap r1-r3-port
sudo ip link set r1-r3-port up


sudo ip tuntap add mode tap r3-r1-port
sudo ip link set r3-r1-port up


sudo ip tuntap add mode tap r3-r4-port
sudo ip link set r3-r4-port up

sudo ip tuntap add mode tap r4-r3-port
sudo ip link set r4-r3-port up


#Creating bridges to connect routers
sudo ovs-vsctl add-br br-R1R2
sudo ovs-vsctl add-br br-R2R3
sudo ovs-vsctl add-br br-R1R3
sudo ovs-vsctl add-br br-R3R4

#Creating ports to connect R1 and R2
sudo ovs-vsctl add-port br-R1R2 r1-r2-port
sudo ovs-vsctl add-port br-R1R2 r2-r1-port

#Creating ports to connect R2 and R3
sudo ovs-vsctl add-port br-R2R3 r2-r3-port
sudo ovs-vsctl add-port br-R2R3 r3-r2-port

#Creating port to connect R1 and R3
sudo ovs-vsctl add-port br-R1R3 r1-r3-port
sudo ovs-vsctl add-port br-R1R3 r3-r1-port


#Creating port to connect R3 and R4
sudo ovs-vsctl add-port br-R3R4 r3-r4-port
sudo ovs-vsctl add-port br-R3R4 r4-r3-port
