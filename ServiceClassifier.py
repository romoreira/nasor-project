'''
Author: Rodrigo Moreira
'''
#Based on NSH Draft: https://tools.ietf.org/id/draft-ietf-sfc-nsh-17.html
#Helpful links (ethertypes): http://www.networksorcery.com/enp/protocol/802/ethertypes.htm
# Run in scapy: sendp(Ether(dst="08:00:27:be:65:6b")/MPLS(label=200)/IPv6(),iface="eth0")

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
from ryu.ofproto import ether
#Temporario
import csv




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


        if (str(datapath.id)) == str(2):
            # install the table-miss flow entry.
            match = parser.OFPMatch(eth_type=0x8847)
            actions = [parser.OFPActionPopMpls(0x86DD),
                       parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                              ofproto.OFPCML_NO_BUFFER)]
            self.add_flow(datapath, 0, match, actions)
            print("Flow Table Created on Switch: "+str(datapath.id))
        else:
            # install the table-miss flow entry.
            match = parser.OFPMatch()
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
            self.add_flow(datapath, 0, match, actions)
            print("Flow Table Created - Switch: "+str(datapath.id))

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


        #______________________________________________________________________________
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return

        packet = Packet(msg.data)
        #self.logger.info("packet: {}".format(msg))
        ether = packet.get_protocol(ryu.lib.packet.ethernet.ethernet)
        ethertype = ether.ethertype
        datapathid_packet_in = datapath.id
        self.logger.info("Switch {} received packet with ethertype: {}".format(datapathid_packet_in, hex(ethertype)))
        ipv6 = packet.get_protocol(ryu.lib.packet.ipv6.ipv6)


        if ethertype == 0x8847:
            mpls = packet.get_protocol(ryu.lib.packet.mpls.mpls)
            ip = mpls.parser(msg.buf)
            self.logger.info("Label: {}, TTL: {}, BSB: {}, EXP: {}".format(mpls.label, mpls.ttl, mpls.bsb, mpls.exp))

            with open('service_mapping.csv') as csvfile:
                service_mapping = csv.reader(csvfile, delimiter=';')
                for row in service_mapping:
                    #print(row[3])
                    #Procure a porta de saida do MPLS Packet_in
                    if str(row[3]) ==  str(mpls.label):
                        # ----APAGAR------
                        dst = eth.dst
                        src = eth.src

                        dpid = datapath.id
                        self.mac_to_port.setdefault(dpid, {})

                        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

                        # learn a mac address to avoid FLOOD next time.
                        self.mac_to_port[dpid][src] = in_port

                        out_port = row[4]
                        out_port = int(out_port)

                        actions = [parser.OFPActionPopMpls(),
                                   parser.OFPActionOutput(out_port)]

                        # install a flow to avoid packet_in next time
                        if out_port != ofproto.OFPP_FLOOD:
                            match = parser.OFPMatch(eth_type=0x8847, mpls_label=mpls.label, in_port=in_port)
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
                        print("Switch: " + str(datapathid_packet_in) + " encaminhou o pacote!\n")
                        return
                        # ----APAGAR------

            print("Não encontrou a porta de saida - saindo")
            return
        else:
            print("Encapsular um header MPLS para ingressar em um LSP")
            # ----APAGAR------
            dst = eth.dst
            src = eth.src

            dpid = datapath.id
            self.mac_to_port.setdefault(dpid, {})

            # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

            # learn a mac address to avoid FLOOD next time.
            self.mac_to_port[dpid][src] = in_port

            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
            else:
                out_port = ofproto.OFPP_FLOOD

            print("IPv6 Source: " + str(ipv6.src))
            #Looking for appropriate MPLS label
            with open('service_mapping.csv') as csvfile:
                service_mapping = csv.reader(csvfile, delimiter=';')
                for row in service_mapping:
                #print(row[3])
                #Procure a porta de saida do MPLS Packet_in
                    if str(row[2]) ==  str(ipv6.src):
                        #print("Funciounou. Label de Saida-> "+str(row[3]))

                        actions = [parser.OFPActionPushMpls(),
                                   parser.OFPActionSetField(mpls_label=int(row[3])),
                                   parser.OFPActionOutput(out_port)]

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
                        print("Switch: " + str(datapathid_packet_in) + " forward a packet with Label: "+str(row[3]+"\n"))
                        return
                print("Unable to forward, service not mapped locally")
            # ----APAGAR------

















        #
        #     if trava == 1:
        #         #Fazer o encaminhamento do pacote com header MPLS
        #         print("Packet_in no Switch: "+str(datapathid_packet_in) + " - nao e switch de ingresso nem de egresso - Encaminhar VIA MPLS: "+str(source_ipv6))
        #         # ----APAGAR------
        #         dst = eth.dst
        #         src = eth.src
        #
        #         dpid = datapath.id
        #         self.mac_to_port.setdefault(dpid, {})
        #
        #         # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        #
        #         # learn a mac address to avoid FLOOD next time.
        #         self.mac_to_port[dpid][src] = in_port
        #
        #         if dst in self.mac_to_port[dpid]:
        #             out_port = self.mac_to_port[dpid][dst]
        #         else:
        #             out_port = ofproto.OFPP_FLOOD
        #
        #         actions = [parser.OFPActionDecMplsTtl(),
        #                    parser.OFPActionOutput(out_port)]
        #
        #         # install a flow to avoid packet_in next time
        #         if out_port != ofproto.OFPP_FLOOD:
        #             match = parser.OFPMatch(eth_type=0x8847, in_port=in_port, eth_dst=dst, eth_src=src)
        #             # verify if we have a valid buffer_id, if yes avoid to send both
        #             # flow_mod & packet_out
        #             if msg.buffer_id != ofproto.OFP_NO_BUFFER:
        #                 self.add_flow(datapath, 1, match, actions, msg.buffer_id)
        #                 return
        #             else:
        #                 self.add_flow(datapath, 1, match, actions)
        #         data = None
        #         if msg.buffer_id == ofproto.OFP_NO_BUFFER:
        #             data = msg.data
        #
        #         out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
        #                                   in_port=in_port, actions=actions, data=data)
        #         datapath.send_msg(out)
        #         print("Switch: " + str(datapathid_packet_in) + " encaminhou o pacote!\n")
        #         # ----APAGAR------
        # else:
        #     print("Packet_in do Tipo MPLS - Fazer nada por enquanto")
        #
        # return
        #
        # for i in range(0, len(switches_list)):
        #     switch_dpid = str(switches_list[i]["dpid"])
        #     switch_dpid = switch_dpid.lstrip("0")
        #     print(switch_dpid)
        #     if switch_dpid == str(datapathid_packet_in):
        #         print("Encontrei o Switch do contexto do packet in: "+str(switch_dpid))
        #
        #
        # return
        #
        #
        # print("***FIM***")
        # return
        #
        #
        # #Check place of packet_in - if is on switch where host is directly connected, it will be a
        # #ingress MPLS domain
        # for i in range(0, len(hosts_list)):
        #     host_datapath_id = hosts_list[i]["port"]["dpid"]
        #     datapathid_packet_in = str(datapathid_packet_in)
        #     host_datapath_id = host_datapath_id.lstrip("0")
        #     if datapathid_packet_in == host_datapath_id:
        #         mpls_label = 0
        #         print("Houve um packet_in no switch onde o host esta diretamente conectado")
        #
        #         print("Switch: "+str(host_datapath_id) + " Porta: "+str(switch_mac_port) + " Host-IP: "+ str(host_ipv6))
        #         #Looking for MPLS Label using 'packet_in' IPv6
        #         with open('service_mapping.csv') as csvfile:
        #             service_mapping = csv.reader(csvfile, delimiter=';')
        #             for row in service_mapping:
        #                 print(row[2])
        #                 if host_ipv6 == row[2]:
        #                     print(row)
        #                     mpls_label = row[3]
        #     else:
        #         print("Packet_IN no switch: "+str(datapathid_packet_in) +" o qual nao possui nenhum host conectado")
        # if mpls_label != None:
        #     print("Label que devera ser utilizado: "+str(mpls_label))
        #
        # return
        # eth_pkt = pkt.get_protocol(ethernet.ethernet)
        # if eth_pkt.ethertype == ether_types.ETH_TYPE_MPLS:
        #     print("O packet_in é MPLS - fazer aqui o pop do header se for a ultima milha")
        #     datapathid_packet_in = str(datapathid_packet_in)
        #     host_datapath_id = host_datapath_id.lstrip("0")
        #     if datapathid_packet_in == host_datapath_id:
        #         ##Fazer aqui o POP do Header MPLS e entregar o Pacote ao Host
        #         return
        # if ipv6:
        #     self.logger.info("IPv6 src: {} dst: {}".format(
        #         ipv6.src, ipv6.dst))
        #
        # print("\n\n\nFim do Programa\n\n\n")
        # return
        # #__________________________________________________________________________
        #
        #
        # if eth.ethertype == ether_types.ETH_TYPE_LLDP:
        #     # ignore lldp packet
        #     return
        # dst = eth.dst
        # src = eth.src
        #
        # dpid = datapath.id
        # self.mac_to_port.setdefault(dpid, {})
        #
        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        # return
        #
        # # learn a mac address to avoid FLOOD next time.
        # self.mac_to_port[dpid][src] = in_port
        #
        # if dst in self.mac_to_port[dpid]:
        #     out_port = self.mac_to_port[dpid][dst]
        # else:
        #     out_port = ofproto.OFPP_FLOOD
        #
        # actions = [parser.OFPActionOutput(out_port)]
        #
        # # install a flow to avoid packet_in next time
        # if out_port != ofproto.OFPP_FLOOD:
        #     match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
        #     # verify if we have a valid buffer_id, if yes avoid to send both
        #     # flow_mod & packet_out
        #     if msg.buffer_id != ofproto.OFP_NO_BUFFER:
        #         self.add_flow(datapath, 1, match, actions, msg.buffer_id)
        #         return
        #     else:
        #         self.add_flow(datapath, 1, match, actions)
        # data = None
        # if msg.buffer_id == ofproto.OFP_NO_BUFFER:
        #     data = msg.data
        #
        # out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
        #                           in_port=in_port, actions=actions, data=data)
        # datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_switch(self, None)  # .topology_api_app
        switches = [switch.dp.id for switch in switch_list]
        print("switches: "+ str(switches))
        links_list = get_link(self, switches[0])  # .topology_api_app ,None
        links = [(link.src.dpid, link.dst.dpid, {'port': link.src.port_no}) for link in links_list]
        print("links_list: "+ str(links_list))
        print("links"+str(links))