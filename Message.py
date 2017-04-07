import json
from NodeInfo import *
from common import *


def create_message_string(title, data):
    return json.dumps({"title": title, "data": data})

class Message:
    def __init__(self, message, sender_address):
        self.title = json.loads(message)['title']
        self.data = json.loads(message)['data']
        self.sender_address = sender_address


class MessageFormat:
    def __init__(self, title, acceptable=True):
        self.title = title
        self.acceptable = acceptable
        self.acceptFrom = []

    def add_accept_from(self, sender_ip):
        self.acceptFrom.append(sender_ip)
        return self

    def set_handler(self, handler_function):
        self.handler = handler_function
        return self


class MessageService:
    def __init__(self, node):
        self.node = node

        from message_formats import defaults
        self.formats_db = defaults  # key: title, value: MessageFormat Object

    def update_message_formats_db(self, items):
        # TODO
        pass

    def handle_message(self, message):
        if self.formats_db[message.title]:
            return self.formats_db[message.title].handler(self.node, message)
        else:
            print "message not recognized: " + message
