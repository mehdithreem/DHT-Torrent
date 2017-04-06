import argparse
from Node import *

# constants
max_num_of_nodes = 400

# messages
request_for_value = "request_for_value"


def dht_hash(key):
    return abs(hash(key)) % (10 ** (len(str(max_num_of_nodes)) + 1)) % max_num_of_nodes


def parse_args():
    # args parsing
    parser = argparse.ArgumentParser(description='DHT-Torrent Client.')

    parser.add_argument('--static', action='store_true', default=False, dest='static', help='Create static node')
    parser.add_argument('--id', action='store', dest='id', type=int, help='This node id')

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


def start():
    args = parse_args()

    my_node = None
    if args.static:
        info = NodeInfo(args.id, "127.0.0.1")
        if args.nextid:
            my_node = create_static_node(args.id, "127.0.0.1", args.nextid, args.nextip)
        else:
            my_node = create_static_node(args.id, "127.0.0.1")

    CLI().printHelp()
    cmd, arg = CLI().getInputCommand()

    if cmd == "INSERT":
        arg = json.loads(arg)
        # my_node.insertValue(arg['key'], arg['value'])
    elif cmd == "INFO":
        my_node.print_info()


if __name__ == '__main__':
    start()
