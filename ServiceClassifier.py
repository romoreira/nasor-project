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
        match = parser.OFPMatch()
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
        mod = parser.OFPFlowMod(datapath=datapath, hard_timeout=10, priority=priority,
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
        self.mac_to_port.setdefault(dpid, {})

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
            #return
        else:
            print("Pacote nao e do tipo NSH")

        msg = ev.msg
        dp = msg.datapath
        dpid = dp.id
        ofproto = dp.ofproto


        # get the received port number from packet_in message.
        print(str(msg.match))
        #in_port = msg.match['eth_type_nxm']
        in_port = msg.match['in_port']
        print("For the first time: "+str(in_port))

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        if dst in self.mac_to_port[dpid]:
            #print("Ja conhece a porta de Entrada - nao fara Flood: " + str(in_port))
            out_port = self.mac_to_port[dpid][dst]
        else:
            print("Nao Conhece a Porta de Entrada - fara Flood")
            out_port = ofproto.OFPP_FLOOD
            #print("Porta de Saida: "+str(out_port))


        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD:
            print("VAI INSTALAR FLOW")
            match = parser.OFPMatch(in_port=in_port, eth_type_nxm=0x894f, nsh_spi=30, nsh_si=3)
            self.add_flow(datapath, 1, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)