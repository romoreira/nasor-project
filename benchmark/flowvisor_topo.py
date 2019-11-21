from mininet.topo import Topo

class FVTopo(Topo):


    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        # Create template host, switch, and link
        #hconfig= {'inNamespace':True}
        #http_link_config= {'bw': 1}
        #video_link_config= {'bw': 10}
        #host_link_config= {}

        # Create switch nodes
        for i in range(4):
            sconfig= {'dpid': "%016x" % (i+1)}
            self.addSwitch('s%d' % (i+1))

        for i in range(4):
            self.addHost('h%d' % (i+1))

        print("Adicionando LINKS")

        self.addLink('s1', 's2')
        self.addLink('s2', 's4')
        self.addLink('s1', 's3')
        self.addLink('s3', 's4')


        self.addLink('h1', 's1')
        self.addLink('h2', 's1')
        self.addLink('h3', 's4')
        self.addLink('h4', 's4')

topos = { 'fvtopo': ( lambda: FVTopo() ) }