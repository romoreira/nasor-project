'''
Author: Rodrigo Moreiar
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

        # install the table-miss flow entry.
        match = parser.OFPMatch("in_port_nxm","eth_dst_nxm")
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        #Flow will be deleted after 10 seconds
        mod = parser.OFPFlowMod(datapath=datapath, idle_timeout=10, hard_timeout=15, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

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
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {'in_port': 2, 'out_port': 3,
            'container_tos': 'cdn',  'spi': 10, 'si': 3,
            'sff_next_hop': '192.168.0.1',
            'nsh_to_sf': 'sf2', 'transport': 'vxlan'})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        print("MAC Origem: "+ str(src))
        print("MAC Destino: "+ str(dst))

        print(str(pkt))
        print(str(eth_pkt.ethertype))
        print(str(ether_types.ETH_TYPE_NSH))

        if eth_pkt.ethertype == ether_types.ETH_TYPE_NSH:
            print("O pacote e do tipo NSH, fazer alguma coisa")
        else:
            print("Pacote nao e do tipo NSH - Faz nada")
            return

        msg = ev.msg
        dp = msg.datapath
        dpid = dp.id
        ofproto = dp.ofproto

        in_port = msg.match['in_port']
        out_port = self.mac_to_port[dpid]['out_port']

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        self.mac_to_port[dpid]['in_port'] = in_port

        print(str(self.mac_to_port))

        #if dst in self.mac_to_port[dpid]:
        #    out_port = self.mac_to_port[dpid][dst]
        #else:
        #    print("Nao Conhece a Porta de Entrada - fara Flood")
        #    out_port = ofproto.OFPP_FLOOD

        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD:
            print("VAI INSTALAR FLOW")
            match = parser.OFPMatch(eth_type_nxm=0x894f, nsh_spi=10, nsh_si=3)
            self.add_flow(datapath, 1, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)