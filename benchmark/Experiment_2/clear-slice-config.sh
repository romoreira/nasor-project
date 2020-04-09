#!/bin/bash

echo "Killing all Router Listenners..."
sudo pgrep -fl python | awk '!/test\.py/{print $1}' | xargs kill

echo "Deleting all SIDs"
sudo srconf localsid del 1::d6

echo "Deleting encapsulation Rulles"
sudo ip -6 route del b::/64