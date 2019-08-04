'''
Author: Rodrigo Moreira
'''
#Based on NSH Draft: https://tools.ietf.org/id/draft-ietf-sfc-nsh-17.html


from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import icmp
from ryu.ofproto import ofproto_v1_3  # This code is OpenFlow 1.0 specific
from ryu.lib.packet.packet import Packet # For packet parsing
import ryu.lib.packet.ipv4
import ryu.lib.packet.mpls
from ryu.controller.handler import set_ev_cls



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

    def pathToNSHFlow(self):
        print("The Package is NSH-based. None flows will be created")
        return

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        msg = ev.msg
        dp = msg.datapath
        # Assumes that datapath ID represents an ascii name
        packet = Packet(msg.data)
        # self.logger.info("packet: {}".format(msg))
        ether = packet.get_protocol(ryu.lib.packet.ethernet.ethernet)
        ethertype = ether.ethertype
        self.logger.info(" Switch {} received packet with ethertype: {}".format("switchName", hex(ethertype)))
        if ethertype == 0x8847:
            mpls = packet.get_protocol(ryu.lib.packet.mpls.mpls)
            self.logger.info("Label: {}, TTL: {}".format(mpls.label, mpls.ttl))
        ipv4 = packet.get_protocol(ryu.lib.packet.ipv4.ipv4)
        if ipv4:
            self.logger.info("IPv4 src: {} dst: {}".format(
                ipv4.src, ipv4.dst))


        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # get the received port number from packet_in message.
        in_port = msg.match['in_port']

        #Tipo MPLS -> 0x8847
        print("\n****Tipo do Pacote passante: " + str(eth_pkt.ethertype))
        if eth_pkt.ethertype == ether_types.ETH_TYPE_MPLS:
            print("***************MPLS***************")
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
            # Learning MAC to avoid flood next time
            self.mac_to_port[dpid][src] = in_port

            msg = ev.msg
            dp = msg.datapath

            packet = Packet(msg.data)
            # self.logger.info("packet: {}".format(msg))
            ether = packet.get_protocol(ryu.lib.packet.ethernet.ethernet)
            ethertype = ether.ethertype
            self.logger.info(" Switch {} received packet with ethertype: {}".format("A", hex(ethertype)))
            if ethertype == 0x8847:
                mpls = packet.get_protocol(ryu.lib.packet.mpls.mpls)
                self.logger.info("Label: {}, TTL: {}".format(mpls.label, mpls.ttl))
            ipv4 = packet.get_protocol(ryu.lib.packet.ipv4.ipv4)
            if ipv4:
                self.logger.info("IPv4 src: {} dst: {}".format(
                    ipv4.src, ipv4.dst))

            print(str(dst))
            print("ESTADO DA MAC TABLE: " + str(self.mac_to_port))

            if dst in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dst]
            else:
                out_port = ofproto.OFPP_FLOOD

            actions = [parser.OFPActionPopMpls(), parser.OFPActionOutput(out_port)]

            if out_port != ofproto.OFPP_FLOOD:
                print("MPLS - A porta de Destino ja e Conhecida Sera feito Flood")
                match = parser.OFPMatch(eth_type_nxm=0x8847, eth_dst=dst)
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
            print("ESTADO DA MAC TABLE: "+str(self.mac_to_port))

        elif eth_pkt.ethertype == ether_types.ETH_TYPE_ARP:
            print("***************ARP***************")
            self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
            #Learning MAC to avoid flood next time
            self.mac_to_port[dpid][src] = in_port

            print("ESTADO DA MAC TABLE: " + str(self.mac_to_port))

            if dst in self.mac_to_port[dpid]:
                print("Aprendeu a porta de entrada - Adicionar Flow")
                out_port = self.mac_to_port[dpid][dst]
                actions = [parser.OFPActionOutput(out_port)]
                #match = parser.OFPMatch(eth_type_nxm=0x8847, eth_dst=dst)
                match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
                if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                    self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                    return
                else:
                    self.add_flow(datapath, 1, match, actions)
            else:
                print("Sempre fazendo Flood")
                out_port = ofproto.OFPP_FLOOD
                actions = [parser.OFPActionOutput(out_port)]
                data = None
                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    data = msg.data
                out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                          in_port=in_port, actions=actions, data=data)
                datapath.send_msg(out)
                print("Flood do ARP Feito")
        else:
            print("***************ICMP***************")
            pkt_icmp = pkt.get_protocol(icmp.icmp)
            if pkt_icmp:

                self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
                self.mac_to_port[dpid][src] = in_port
                print("ESTADO DA MAC TABLE: " + str(self.mac_to_port))

                if dst in self.mac_to_port[dpid]:
                    out_port = self.mac_to_port[dpid][dst]
                else:
                    out_port = ofproto.OFPP_FLOOD

                actions = [parser.OFPActionOutput(out_port)]

                # install a flow to avoid packet_in next time
                if out_port != ofproto.OFPP_FLOOD:
                    print("nao flood - icmp")
                    match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
                    #match = parser.OFPMatch(eth_type_nxm=0x8847, in_port=in_port, eth_dst=dst, eth_src=src)
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

        print("FIM ")
        return