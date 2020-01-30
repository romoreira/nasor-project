#!/bin/bash

sudo ovs-vsctl add-br br-ABBA
sudo ovs-vsctl add-br br-AC
sudo ovs-vsctl add-br br-CB

sudo ovs-vsctl add-port br-ABBA peeringA-B
sudo ovs-vsctl add-port br-ABBA peeringB-A

sudo ovs-vsctl add-port br-AC peeringA-C
sudo ovs-vsctl add-port br-AC peeringC-A

sudo ovs-vsctl add-port br-CB peeringB-C
sudo ovs-vsctl add-port br-CB peeringC-B
