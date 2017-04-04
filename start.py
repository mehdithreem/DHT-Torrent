import argparse
from socket import *

# constants
max_num_of_nodes = 400

class NodeInfo:
    def __init__(self, id, ip):
        self.id = int(id)
        self.ip = str(ip)

class Node:
    def __init__(self, myInfo):
        self.myInfo = myInfo
        self.nextNodes = list()
        self.hashTable = dict()
        self.socket = Socket()

    def setNextInfo(self, nextInfo):
        self.nextNodes.append(nextInfo)

    def addKeyValue(self, key, value):
        self.hashTable[key] = value

def hash(key):
    return abs(hash(key)) % (10 ** (len(str(max_num_of_nodes)) + 1)) % max_num_of_nodes

def parseArgs():
    # args parsing
    parser = argparse.ArgumentParser(description='DHT-Torrent Client.')

    parser.add_argument('--static', action='store_true', default=False, dest='static',  help='Create static node')
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
        INSERT [key, value]'''

    def getInputCommand(self):
        inputLine = raw_input()
        cmd = inputLine.split(" ")[0]
        return cmd, inputLine.split(" ")[1:]

def start():
    args = parseArgs()

    mynode = None
    if args.static:
        info = NodeInfo(args.id, "127.0.0.1")
        mynode = Node(info) #TODO: set ip
        if args.nextid != None:
            mynode.setNextInfo(NodeInfo(args.nextid, args.nextip))

if __name__ == '__main__':
    start()
