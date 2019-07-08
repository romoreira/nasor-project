# Edge Computing Slice
Edge Computing Slice aims to provide network and computing sharing resources to handle many user applications with special requirements over the unique infrastructure.

Here we bring some steps to follow to deploy and try our solution.

1. **Raspberry Installation**

* Download Raspberry Image: [Raspbian Buster with desktop and recommended software](https://www.balena.io/etcher/)
* Extract ISO file in a directory
* Uses a tool to mount ISO image on Raspberry SD-Card [Etcher](https://www.balena.io/etcher/)
* Start your Raspberry for the first time (make it updated)

2. **Installing OpenvSwitch on Raspberry**
* Go to OVS page and download a desired release (>2.9.0 is required to work with NSH protocol) [2.10.9](https://www.openvswitch.org/releases/openvswitch-2.10.0.tar.gz)
* Extract tar file: $tar -zxvf <ovs.tar.gz>
* Open Extracted files on OVS directory: $ cd ovs
  * Run: $ ./boot
  * Run: $ ./configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc (_Mandatory to LXD runs OVS commands_)
  * Run: $ sudo make
  * Run: $ sudo make install
* Setting up OVS:
  * Run: $ export PATH=$PATH:/usr/share/openvswitch/scripts
  * Run: $ ovs-ctl start (Here all OVS deamons will run and OVS database will be populated)
* Try OVS:
  * Run: # ovs-vsctl show



[Rodrigo Moreira](http://twitter.com/moreira_r) \
*E-mail*:
![alt text](https://github.com/romoreira/EdgeComputingSlice/blob/master/mail.PNG)

