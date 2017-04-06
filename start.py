import argparse
import fcntl
import struct
import sys
import logging
from Node import *
from common import *


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def parse_args():
    # args parsing
    parser = argparse.ArgumentParser(description='DHT-Torrent Client.')

    parser.add_argument('--static', action='store_true', default=False, dest='static', help='Create static node')
    parser.add_argument('--id', action='store', dest='id', type=int, help='This node id')
    parser.add_argument('--ip', action='store', dest='ip', help='This node ip')

    parser.add_argument('--nextpeerid', action='store', dest='nextid', type=int, default=None, help='Next node ID')
    parser.add_argument('--nextpeerip', action='store', dest='nextip', default=None, help='Next node IP address')

    parser.add_argument('--dynamic', action='store_true', default=False, dest='dynamic',
                        help='Create dynamic node')
    parser.add_argument('--file', action='store', dest='filePath', help='Path of torrent system info file')

    return parser.parse_args()

class CLI:
    def printHelp(self):
        print '''
        INSERT {"key": KEY, "value": VALUE}'''

    def getInputCommand(self):
        inputLine = raw_input()
        cmd = inputLine.split(" ")[0]

        return cmd, ''.join(inputLine.split(" ")[1:])


def setup_logging():
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)


def start():
    setup_logging()
    args = parse_args()

    my_node = None
    if args.static:
        if args.nextid:
            my_node = create_static_node(args.id, args.ip, args.nextid, args.nextip)
        else:
            my_node = create_static_node(args.id, args.ip)

    while True:
        my_node.socket.run()
        log.debug("\n" + my_node.__str__())

    CLI().printHelp()
    cmd, arg = CLI().getInputCommand()

    if cmd == "INSERT":
        arg = json.loads(arg)
        my_node.insert_value(arg['key'], arg['value'])
    elif cmd == "INFO":
        my_node.print_info()


if __name__ == '__main__':
    start()
