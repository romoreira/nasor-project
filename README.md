# Edge Computing Slice
Edge Computing Slice aims to provide network and computing sharing resources to handle many user applications with special requirements over the unique infrastructure.

Here we bring some steps to follow to deploy and try our solution.

## **Raspberry Installation**

* Download Raspberry Image: [Raspbian Buster with desktop and recommended software](https://www.balena.io/etcher/)
* Extract ISO file into directory
* Use a tool to mount ISO image on Raspberry SD-Card [Etcher](https://www.balena.io/etcher/)
* Start your Raspberry for the first time (make it updated)

## **Ansible Playbook Installation** [Site](https://docs.ansible.com/ansible/latest/installation_guide/index.html)
* Steps:
  * Run: $ sudo apt-get install software-properties-common
  * Run: $ git clone git://github.com/ansible/ansible.git --recursive
  * Run: $ cd ansible/
  * Run: $ git checkout v2.2.0.0-1
  * Run: $ make deb
  * Run: $ cd deb-build/unstable/
  * Run: $ sudo dpkg -i ansible_2.2.0.0-100.git201611010320.cdec853e37.HEAD~unstable_all.deb
  * Run: $ sudo pip install pyyaml
  * Run: $ ansible --version (_to check if ansible is correctly installed_)

### Configuring hosts on Ansible Controller Node
* Put host names into /etc/hosts properly
* Edit /etc/ansible/hosts -> insert host name
  * hostname ansible_user=user
* On Server:
  * Create SSH Keys: $ ssh-keygen (_without passphrase_)
  * Put the Public key into Server (Edge Node) which you will be connected remotely: $ ssh-copy-id user@host (_in this time will be necessary to insert pass for the first time_)
  > Usually keys are created here: /home/username/.ssh
* On Client:
  * Make SSH service on Client (which will receive ssh connections from Server) accept only connections using Key file:
    * Edit: $ sudo vim /etc/ssh/sshd_config
    * Insert: "PubkeyAuthentication yes"
    * Restart SSH service: $ systemctl reload sshd
* Try SSH connection from Server to Node (in this time any pass should be required): $ ssh user@host
* Try Ansible: $ ansible all -m ping (if any success message appear check ssh keys)
> The point is: Server (SSH) creates keys and have to put it on Client (Edge node). \
> Aditional Ansible commands can be found [here](https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html).

## **Installing OpenvSwitch on Raspberry**
* Dependences to compile OVS source:
  * Run: $ sudo apt-get install gcc flex bison
  * Run: $ sudo apt-get install bridge-utils
  * Run: $ sudo apt-get install make
  * Run: $ sudo apt-get install autoconf
  * Run: $ sudo apt-get install autoconf automake libtool perl graphviz bridge-utils git (**LXD requires _Linux Bridge_ installed**)
* Go to OVS page and download a desired release (>2.9.0 is required to work with NSH protocol) [2.10.0](https://www.openvswitch.org/releases/openvswitch-2.10.0.tar.gz)
* Extract tar file: $tar -zxvf <ovs.tar.gz>
* Open Extracted files on OVS directory: $ cd ovs
  * Run: $ ./boot
  * Run: $ ./configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc (**Mandatory to LXD runs OVS commands**)
  * Run: $ sudo make
  * Run: $ sudo make install
* Setting up OVS:
  * Run: $ export PATH=$PATH:/usr/share/openvswitch/scripts
  * Run: $ ovs-ctl start (_Here all OVS deamons will run and OVS database will be populated_)
* Try OVS:
  * Run: # ovs-vsctl show

## **Installing LXD (as snap) on Raspberry**
* Run: $ sudo apt-get install snap snapd
* Run: $ sudo snap install lxd
* Run: $ . /etc/profile.d/apps-bin-path.sh (_to put LXD commands available on bash_)
* Run: $ lxd init
* Run: # lxc launch ubuntu:16.04 _container-name_
* Run: # lxc network set testbr0 bridge.driver openvswitch (_to change LXD network driver to OVS_)
* Run: # lxc list

## **Installing and Configuring Docker to [Use OpenvSwitch](http://containertutorials.com/network/ovs_docker.html)**
* Follow the official Docker installation tutorial available [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* Once you already have Docker running, you have to configure Docker to use OvS.
* Installing OvS Docker Utility
  * Run: $ cd /usr/bin
  * Run: $ sudo wget https://raw.githubusercontent.com/openvswitch/ovs/master/utilities/ovs-docker
  * Run: $ sudo chmod a+rwx ovs-docker
* Add a port from OvS bridge to the Docker Container
  * Run: $ sudo docker run -t -i --name container1 ubuntu /bin/bash
  * Run: $ sudo docker run -t -i --name container2 ubuntu /bin/bash
* Connecting the container to the OvS Bridge
  * Run: $ ovs-docker add-port ovs-br1 eth1 container1 --ipaddress=<>/24
  * Run: $ ovs-docker add-port ovs-br1 eth1 container2 --ipaddress=<>/24

## **Installing Seguiment Routing on Linux (Debian Release)**
  ### **Upgrade the Kernel to [4.19](https://elixir.bootlin.com/linux/v4.19.1/source/net/ipv6/route.c)**
  * `wget -c http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.19/linux-headers-4.19.0-041900_4.19.0-041900.201810221809_all.deb`

  * `wget -c http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.19/linux-headers-4.19.0-041900-generic_4.19.0-041900.201810221809_amd64.deb`

  * `wget -c http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.19/linux-image-unsigned-4.19.0-041900-generic_4.19.0-041900.201810221809_amd64.deb`

  * `wget -c http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.19/linux-modules-4.19.0-041900-generic_4.19.0-041900.201810221809_amd64.deb`
  * `wget archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb`
  * Run: $ sudo dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb
  * `wget security.ubuntu.com/ubuntu/pool/main/l/linux-base/linux-base_4.5ubuntu1~16.04.1_all.deb`
  * Run: $ sudo dpkg -i linux-base_4.5ubuntu1~16.04.1_all.deb
  * Run: $ sudo dpkg -i linux-h*.deb
  * Run: $ sudo dpkg -i linux-im*.deb
  * Run: $ sudo dpkg -i linux-mo*.deb

> Additional steps can be found [here](https://github.com/netgroup/SRv6-net-prog/)

## **Installing Apache [Geode](https://geode.apache.org)**
* In a new VM (or cluster) follow the steps below:
1. `sudo apt-get install default-jre openjdk-8-jre-headless default-jdk unzip`
2. `export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64`
3. `wget http://ftp.unicamp.br/pub/apache/geode/1.9.1/apache-geode-1.9.1-src.tgz` (the link can change on time - because new released)
4. `tar -zxvf apache-geode-1.9.1-src.tgz`
5. `cd apache-geode-1.9.1-src/`
6. `./gradlew build -Dskip.tests=true`

## **Running Apache [Geode](https://geode.apache.org) in our E2E Orchestration Environment**
* In a new VM (or in one which is member of cluster) follow the spteps below:
1. `mkdir my_geode`
2. `cd /home/ubuntu/my_geode`
3. `/home/ubuntu/apache-geode-1.9.1-src/geode-assembly/build/install/apache-geode/bin/gfsh`
4. `start locator --name=locator1`
5. `configure pdx --read-serialized=true --disk-store`
6. `start server --name=server1 --start-rest-api=true --http-service-port=1026 --http-service-bind-address=200.19.151.175`
7. `create region --name=regionA --type=REPLICATE_PERSISTENT`

> TIP: Now thw RestAPI should be working fine (check it)


[Rodrigo Moreira](http://twitter.com/moreira_r) \
*E-mail*:
![alt text](https://github.com/romoreira/EdgeComputingSlice/blob/master/mail.PNG)

