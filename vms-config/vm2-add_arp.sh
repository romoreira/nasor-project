#!/bin/bash
ip -6 neigh add 2001:470:28:5b2::3 lladdr 08:00:27:19:6e:a7 dev eth0
echo "Static ARP Added"
