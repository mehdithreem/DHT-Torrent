from Message import MessageFormat
from Node import *
from NodeInfo import *

def SET_PREV_handler(node, message):
    node.set_prev_info(NodeInfo(message.data['id'], message.data['ip']))
    log.info("prev_node set on " + node.myInfo.to_str())

def DHT_INSERT__KEY_SEARCH(node, message):
    node.find_proper_node_for_key(message.data['key'], message.data['ip'])

def DHT_INSERT__GET_VALUE(node, message):
    log.debug("DHT_INSERT__GET_VALUE call")
    return node.fetch_pending_value(message.data['key'])

# messages are json objects:
# { "title" : TITLE, "data" : DATA }
defaults = \
    {
        "SET_PREV": MessageFormat("SET_PREV").set_handler(SET_PREV_handler),
        "DHT_INSERT__KEY_SEARCH": MessageFormat("DHT_INSERT__KEY_SEARCH").set_handler(DHT_INSERT__KEY_SEARCH),
        "DHT_INSERT__GET_VALUE": MessageFormat("DHT_INSERT__GET_VALUE").set_handler(DHT_INSERT__GET_VALUE)
    }
