from SocketService import *
from Message import *
from NodeInfo import *
import json


def dht_hash(key):
    return abs(hash(key)) % (10 ** (len(str(max_num_of_nodes)) + 1)) % max_num_of_nodes

class Node:
    def __init__(self, node_id, node_ip):
        self.myInfo = NodeInfo(node_id, node_ip)
        self.nextNode = None
        self.prevNode = None
        # self.hashTable = dict()
        self.socket = SocketService(self)
        self.message = MessageService(self)

    def __str__(self):
        return_str = "DHT-Torrent Node " + str(self.myInfo.id) + "@" + self.myInfo.ip + "\n"
        if self.nextNode:
            return_str += "\tNext Node: " + str(self.nextNode.id) + "@" + str(self.nextNode.ip) + "\n"
        if self.prevNode:
            return_str += "\tPrev Node: " + str(self.prevNode.id) + "@" + str(self.prevNode.ip) + "\n"
        # TODO: print database
        return return_str

    def set_next_info(self, next_info):
        self.nextNode = next_info

    def set_prev_info(self, prev_info):
        self.prevNode = prev_info

    def print_info(self):
        print self

    def insertValue(self, key, value):
        hashedKey = DHT_hash(key)
        if hashedKey <= self.myInfo.id:
            self.hashTable[hashedKey] = value
            return

        self.findProperNodeForInsert(hashedKey, self.myInfo.ip)

        target_ip = self.socket.lookForMessage(request_for_value)
        self.socket.sendMessage(target_ip, value)

    def findProperNodeForInsert(self, hashedKey, ip):
        if hashedKey > self.myInfo.id:
            self.socket.sendMessage(self.nextNode.ip, json.dump({'key': hashedKey, 'ip': ip}))
        else:
            self.socket.sendMessage(ip, request_for_value)
            value = self.socket.recvMessage(ip)
            self.hashTable[hashedKey] = value


def create_static_node(node_id, node_ip, next_node_id=None, next_node_ip=None):

    node = Node(node_id, node_ip)

    if next_node_ip:
        node.set_next_info(NodeInfo(next_node_id, next_node_ip))

        # call next node to set its prev node
        node.socket.send_message(
            next_node_ip,
            json.dumps({"title": "SET_PREV", "data": {"id": node_id, "ip": node_ip}})
        )
        log.info("node_ip " + node_ip + " sent to " + str(next_node_id) + "@" + next_node_ip)

    return node
