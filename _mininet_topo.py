# !/usr/bin/python

# sudo mn --custom _mininet_topo.py --topo mytopo,5
# sudo mn --custom _mininet_topo.py --topo mytopo,3 --test simpletest
# or just run this python file

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."

    def build(self):
        # switch = self.addSwitch('s1')
        # # Python's range(N) generates 0..N-1
        # for h in range(n):
        #     host = self.addHost('h%s' % (h + 1))
        #     self.addLink(host, switch)

        s1 = self.addSwitch('s1')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)
        self.addLink(h5, s1)
        self.addLink(h6, s1)

#
def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo()
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    # net.stop()

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')


    for host in [h1, h2, h3, h4, h5, h6]:
        host.cmdPrint('cd /media/sf_DHT-Torrent')

    h1.cmdPrint('echo \'python /media/sf_DHT-Torrent/start.py --static --id 600 --ip ' + h1.IP() + ' \' > h1.sh')
    h2.cmdPrint('echo \'python /media/sf_DHT-Torrent/start.py --static --id 500 --ip ' + h2.IP() + " --nextpeerid 600 --nextpeerip " + h1.IP() + ' \' > h2.sh')
    h3.cmdPrint('echo \'python /media/sf_DHT-Torrent/start.py --static --id 400 --ip ' + h3.IP() + " --nextpeerid 500 --nextpeerip " + h2.IP() + ' \' > h3.sh')
    h4.cmdPrint('echo \'python /media/sf_DHT-Torrent/start.py --static --id 300 --ip ' + h4.IP() + " --nextpeerid 400 --nextpeerip " + h3.IP() + ' \' > h4.sh')
    h5.cmdPrint('echo \'python /media/sf_DHT-Torrent/start.py --static --id 200 --ip ' + h5.IP() + " --nextpeerid 300 --nextpeerip " + h4.IP() + ' \' > h5.sh')
    h6.cmdPrint('echo \'python /media/sf_DHT-Torrent/start.py --static --id 100 --ip ' + h6.IP() + " --nextpeerid 200 --nextpeerip " + h5.IP() + ' \' > h6.sh')

    # h1.cmdPrint('ls')

    net.startTerms()
    CLI(net)
    # CLI(net).do_xterm(h1)

    net.stopXterms()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()

topos = { 'mytopo': SingleSwitchTopo }
# tests = { 'mytest': simpleTest }