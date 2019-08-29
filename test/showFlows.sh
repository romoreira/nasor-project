!#/bin/bash
echo "___________________SW1_______________________________"
sudo  ovs-appctl bridge/dump-flows br-int
echo "___________________SW2_______________________________"
sudo  ovs-appctl bridge/dump-flows br-int2
echo "___________________SW3_______________________________"
sudo  ovs-appctl bridge/dump-flows br-int3
echo "_____________________________________________________"
