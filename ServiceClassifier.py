'''
Author: Rodrigo Moreira
'''
#Based on NSH Draft: https://tools.ietf.org/id/draft-ietf-sfc-nsh-17.html



from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.lib.packet import packet
from ryu.lib.packet import ether_types
from ryu.ofproto import ofproto_v1_3  # This code is OpenFlow 1.0 specific
import ryu.lib.packet.ipv4
import ryu.lib.packet.ipv6
import ryu.lib.packet.mpls
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet.packet import Packet
from ryu.lib.packet import ipv6,ethernet
from ryu.topology.api import get_switch, get_link, get_host
import requests
import json
import sys



class Classifier(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Classifier, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        print("Getting Slices Details...")

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        print("Flow Table Created")

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        #Flow will be deleted after 10 seconds - idle_timeout = 15
        mod = parser.OFPFlowMod(datapath=datapath, idle_timeout=15, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)
        print("------>Flow Added!")

    def find_protocol(self, pkt, name):
        for p in pkt.protocols:
            if p.protocol_name == name:
                return p

    def pathToMPLSFlow(self):
        URL = "http://10.0.0.100:8080/v1.0/topology/links"
        r = requests.get(url=URL)
        data = r.json()
        print("LINKS: " + str(data))

        URL = "http://10.0.0.100:8080/v1.0/topology/switches"
        r = requests.get(url=URL)
        data = r.json()
        print("SWTCHES: " + str(data))

        URL = "http://10.0.0.100:8080/v1.0/topology/hosts"
        r = requests.get(url=URL)
        data = r.json()
        print("HOSTS: " + str(data))
        return data

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        #________________________________________________________
        print("Ola mundo")
        packet = Packet(msg.data)
        # self.logger.info("packet: {}".format(msg))
        ether = packet.get_protocol(ryu.lib.packet.ethernet.ethernet)
        ethertype = ether.ethertype
        datapathid = datapath.id
        self.logger.info("Switch {} received packet with ethertype: {}".format(datapathid, hex(ethertype)))
        ipv6 = packet.get_protocol(ryu.lib.packet.ipv6.ipv6)
        print(ipv6)

        URL = "http://10.0.0.100:8080/v1.0/topology/hosts"
        r = requests.get(url=URL)
        hosts_list = r.json()
        print("HOSTS: " + str(json.dumps(hosts_list)))
        hosts_list = json.loads(str(json.dumps(hosts_list)))
        print(len(hosts_list))
        for i in range(0, len(hosts_list)):
            i = int(i)
            host_ipv6 = hosts_list[i]["ipv6"]
            host_mac = hosts_list[i]["mac"]
            switch_mac_port = hosts_list[i]["port"]["hw_addr"]
            switch_dpid =  hosts_list[i]["port"]["dpid"]
            switch_port_name = hosts_list[i]["port"]["name"]
            print("Porta do Switch que o Host  esta conectado: "+str(switch_mac_port))


        URL = "http://10.0.0.100:8080/v1.0/topology/switches"
        r = requests.get(url=URL)
        data = r.json()
        #print("SWTCHES: " + str(data))
        print("DUMPS: "+str(json.dumps(data)))
        data = json.loads(str(json.dumps(data)))
        print(data[0]["ports"][0]["hw_addr"])
        print(len(data))


        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        if eth_pkt.ethertype == ether_types.ETH_TYPE_MPLS:
            print("O packet_in é MPLS - fazer aqui o pop do header se for a ultima milha")
        if ipv6:
            self.logger.info("IPv6 src: {} dst: {}".format(
                ipv6.src, ipv6.dst))
        #________________________________________________________


        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_switch(self, None)  # .topology_api_app
        switches = [switch.dp.id for switch in switch_list]
        print("switches: "+ str(switches))
        links_list = get_link(self, switches[0])  # .topology_api_app ,None
        links = [(link.src.dpid, link.dst.dpid, {'port': link.src.port_no}) for link in links_list]
        print("links_list: "+ str(links_list))
        print("links"+str(links))