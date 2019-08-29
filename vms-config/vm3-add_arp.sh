#!/bin/bash
#ip -6 neigh del 2001:470:28:5b2::2 dev eth0
ip -6 neigh add 2001:470:28:5b2::2 lladdr 08:00:27:be:65:6b dev eth0
echo "Static ARP Added"

