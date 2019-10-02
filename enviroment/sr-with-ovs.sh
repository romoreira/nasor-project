#!/bin/bash

#Creating Ingress IF and add It to Switch: sr-br
sudo ip tuntap add mode tap ingress
sudo ifconfig ingress up
sudo ovs-vsctl add-port sr-br ingress

#Creating Ingress and Egress IF and add they to Switch: sr-br
sudo ip tuntap add mode tap in-nfv
sudo ifconfig in-nfv up
sudo ip tuntap add mode tap out-nfv
sudo ifconfig out-nfv up
sudo ovs-vsctl add-port sr-br in-nfv
sudo ovs-vsctl add-port sr-br out-nfv

#Creating Egress IF and add it to Switch: sr-br
sudo ip tuntap add mode tap egress
sudo ifcofig egress up
sudo ovs-vsctl add-port sr-br egress
