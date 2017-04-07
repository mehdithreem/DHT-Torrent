import socket
import select
from Message import *
from common import *


SERVER_PORT = 12000
CLIENT_PORT = 12001


class SocketService:
    def __init__(self, node, port=SERVER_PORT, number_of_sender=4, ip="0.0.0.0", buffer_size=10240):
        self.node = node
        self.READER_LIST = []
        self.WRITER_LIST = []
        self.RECV_BUFFER = buffer_size
        self.PORT = port

        # starting server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, self.PORT))
        self.server_socket.listen(number_of_sender)

        self.READER_LIST.append(self.server_socket)

        log.info("node " + str(self.node.myInfo.id) + "@" + self.node.myInfo.ip + " server started")

        self.ADDR_DB = {}  # key: socket fd, value: address
        self.CLIENT_CONNECTIONS = {}  # key: server_ip, value: socket

    def __del__(self):
        self.server_socket.close()
        for key in self.CLIENT_CONNECTIONS.keys():
            self.CLIENT_CONNECTIONS[key].close()

    def run(self):
        read_sockets, write_sockets, error_sockets = select.select(self.READER_LIST, self.WRITER_LIST, [], 2)

        # for sock in write_sockets:
        #     pass

        for sock in read_sockets:
            if sock == self.server_socket:
                # accept new connection
                sock_fd, addr = self.server_socket.accept()

                self.ADDR_DB[sock_fd] = addr
                self.READER_LIST.append(sock_fd)

                log.info("node " + self.node.myInfo.to_str() + " accepted connection from " + addr[0])
            else:
                # handle new request
                try:
                    data = sock.recv(self.RECV_BUFFER)
                    log.info(self.node.myInfo.to_str() + " received a message from " + self.ADDR_DB[sock][0] + " : " + data)
                    response = self.node.message.handle_message(Message(data, self.ADDR_DB[sock][0]))

                    if response:
                        sock.sendall(response)
                        log.info("response has sent to " + self.ADDR_DB[sock][0])
                except:
                    # if connection is closed
                    sock.close()
                    log.info(self.ADDR_DB[sock][0] + " left node " + self.node.myInfo.to_str())
                    self.READER_LIST.remove(sock)
                    del self.ADDR_DB[sock]

    def send_message(self, server_ip, message, need_reply=False):
        client_socket = self.CLIENT_CONNECTIONS.get(server_ip)
        if not client_socket:
            log.info(self.node.myInfo.to_str() + " created a connection with " + server_ip)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, SERVER_PORT))
            self.CLIENT_CONNECTIONS[server_ip] = client_socket

        client_socket.sendall(message)

        if need_reply:
            reply = client_socket.recv(self.RECV_BUFFER)
            return reply
