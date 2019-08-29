#!/bin/bash
echo "Creating Bridges"
sudo ovs-vsctl add-br br-int
sudo ovs-vsctl add-br br-int2
sudo ovs-vsctl add-br br-int3
echo "Bridge Created"
sudo ifconfig br-int up
sudo ifconfig br-int 10.0.0.10/24
sudo ifconfig br-int2 up
sudo ifconfig br-int2 10.0.0.20/24
sudo ifconfig br-int3 up
sudo ifconfig br-int3 10.0.0.30/24
echo "Bridge Updated"
sudo ip link add veth0 type veth peer name veth1
sudo ip link add veth2 type veth peer name veth3
sudo ifconfig veth0 up
sudo ifconfig veth1 up
sudo ifconfig veth2 up
sudo ifconfig veth3 up
sudo ovs-vsctl add-port br-int veth0
sudo ovs-vsctl add-port br-int2 veth1
sudo ovs-vsctl add-port br-int2 veth2
sudo ovs-vsctl add-port br-int3 veth3
echo "Changing Switch Name"
sudo ovs-vsctl set bridge br-int other_config:datapath-id=0000000000000001
sudo ovs-vsctl set bridge br-int2 other_config:datapath-id=0000000000000002
sudo ovs-vsctl set bridge br-int3 other_config:datapath-id=0000000000000003
echo "Done!"
