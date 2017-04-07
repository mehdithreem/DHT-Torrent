from time import sleep

from SocketService import *
from Message import *
from NodeInfo import *
import message_formats as mf
import json
import sys


def dht_hash(key):
    return abs(hash(key)) % (10 ** (len(str(max_num_of_nodes)) + 1)) % max_num_of_nodes


class Node:
    def __init__(self, node_id, node_ip):
        self.myInfo = NodeInfo(node_id, node_ip)
        self.nextNode = None  # next id should be greater than self id
        self.prevNode = None  # prev id should be less than self id
        self.hashTable = dict()
        self.pendingValues = dict()
        self.foundedValues = dict()
        self.socket = SocketService(self)
        self.message = MessageService(self)

    def __str__(self):
        return_str = "DHT-Torrent Node " + str(self.myInfo.id) + "@" + self.myInfo.ip + "\n"
        if self.nextNode:
            return_str += "\tNext Node: " + str(self.nextNode.id) + "@" + str(self.nextNode.ip) + "\n"
        if self.prevNode:
            return_str += "\tPrev Node: " + str(self.prevNode.id) + "@" + str(self.prevNode.ip) + "\n"
        if len(self.hashTable):
            return_str += "\n====== HashTable ======\n"
            for key in self.hashTable:
                return_str += str(key) + " :: " + self.hashTable[key] + "\n"
        return return_str

    def to_str(self):
        return self.__str__()

    def set_next_info(self, next_info):
        self.nextNode = next_info

    def set_prev_info(self, prev_info):
        self.prevNode = prev_info

    def insert_value(self, key, value):
        hashed_key = dht_hash(key)
        hashed_key = int(key)  # TODO: remove this
        prev_id = self.prevNode.id if self.prevNode else -float('Inf')
        if prev_id < hashed_key < self.myInfo.id:
            self.hashTable[hashed_key] = value
            log.info("{" + str(key) + "::" + value + "} inserted directly into " + self.myInfo.to_str())
            return

        self.find_proper_node_for_key(hashed_key, self.myInfo.ip)
        self.pendingValues[hashed_key] = value
        log.info("{" + str(key) + "::" + value + "} pending in " + self.myInfo.to_str())

    def fetch_pending_value(self, key):
        value = self.pendingValues[key]
        log.info("{" + str(key) + "::" + value + "} fetched from pending in " + self.myInfo.to_str())
        del self.pendingValues[key]
        return value

    def find_proper_node_for_key(self, hashed_key, ip):
        prev_id = self.prevNode.id if self.prevNode else -float('Inf')
        if hashed_key > self.myInfo.id and self.nextNode:
            self.socket.send_message(self.nextNode.ip, create_message_string("DHT_INSERT__KEY_SEARCH", {'key': hashed_key, 'ip': ip}))
            log.info("insert {" + str(hashed_key) + "@" + ip + "} sent to " + self.nextNode.to_str())
        elif prev_id >= hashed_key:
            self.socket.send_message(self.prevNode.ip, create_message_string("DHT_INSERT__KEY_SEARCH", {'key': hashed_key, 'ip': ip}))
            log.info("insert {" + str(hashed_key) + "@" + ip + "} sent to " + self.prevNode.to_str())
        else:
            log.info("{" + str(hashed_key) + "@" + ip + "} will be save to " + self.myInfo.to_str())
            value = self.socket.send_message(ip, create_message_string("DHT_INSERT__GET_VALUE", {'key': hashed_key}), True)
            self.hashTable[hashed_key] = value
            log.info("{" + str(hashed_key) + "::" + value + "} saved to " + self.myInfo.to_str())

    def lookup_key(self, key):
        hashed_key = dht_hash(key)
        hashed_key = int(key)  # TODO: remove this
        prev_id = self.prevNode.id if self.prevNode else -float('Inf')
        if prev_id < hashed_key < self.myInfo.id:
            value = self.hashTable[hashed_key]
            log.info("{" + str(key) + "::" + value + "} directly found in " + self.myInfo.to_str())
            return value

        self.lookup_recursive(hashed_key, self.myInfo.ip)
        log.info("searching for " + str(key))
        while not self.foundedValues.get(hashed_key):
            self.socket.run()

        value = self.foundedValues[hashed_key]
        del self.foundedValues[hashed_key]

        log.info("{" + str(key) + "::" + value + "} found")

        return value

    def add_founded_value(self, key, value):
        self.foundedValues[key] = value

    def lookup_recursive(self, hashed_key, ip):
        prev_id = self.prevNode.id if self.prevNode else -float('Inf')
        if hashed_key > self.myInfo.id and self.nextNode:
            self.socket.send_message(self.nextNode.ip, create_message_string(mf.DHT_LOOKUP__KEY_SEARCH, {'key': hashed_key, 'ip': ip}))
            log.info("lookup {" + str(hashed_key) + "#" + ip + "} sent to " + self.nextNode.to_str())
        elif prev_id >= hashed_key:
            self.socket.send_message(self.prevNode.ip, create_message_string(mf.DHT_LOOKUP__KEY_SEARCH, {'key': hashed_key, 'ip': ip}))
            log.info("lookup {" + str(hashed_key) + "#" + ip + "} sent to " + self.prevNode.to_str())
        else:
            log.info("{" + str(hashed_key) + "#" + ip + "} found at " + self.myInfo.to_str())
            value = self.hashTable.get(hashed_key)
            self.socket.send_message(ip, create_message_string(mf.DHT_LOOKUP__FOUND_VAL, {'key': hashed_key, 'value': value}))
            log.info("{" + str(hashed_key) + "::" + value + "} sent to " + ip)


def create_static_node(node_id, node_ip, next_node_id=None, next_node_ip=None):
    node = Node(node_id, node_ip)

    if next_node_ip:
        if next_node_id <= node_id:
            log.error("Next id should be greater than self id")
            sys.exit(1)

        node.set_next_info(NodeInfo(next_node_id, next_node_ip))

        # call next node to set its prev node
        node.socket.send_message(
            next_node_ip,
            json.dumps({"title": "SET_PREV", "data": {"id": node_id, "ip": node_ip}})
        )
        log.info("node_ip " + node_ip + " sent to " + str(next_node_id) + "@" + next_node_ip)

    return node
