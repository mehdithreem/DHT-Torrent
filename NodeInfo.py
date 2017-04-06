class NodeInfo:
    def __init__(self, node_id, node_ip):
        self.id = node_id
        self.ip = node_ip

    def __str__(self):
        return str(self.id) + "@" + self.ip

    def to_str(self):
        return self.__str__()