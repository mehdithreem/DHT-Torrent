import socket
import select
from Message import *

SERVER_PORT = 12000
CLIENT_PORT = 12001


class SocketService:
    def __init__(self, node, port=SERVER_PORT, number_of_sender=4, ip="127.0.0.1", buffer_size=4096):
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

        self.ADDR_DB = {}  # key: socket fd, value: address
        # self.inbox = {}

    def __del__(self):
        self.server_socket.close()

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(self.READER_LIST, self.WRITER_LIST, [])

            # for sock in write_sockets:
            #     pass

            for sock in read_sockets:
                if sock == self.server_socket:
                    # accept new connection
                    sock_fd, addr = self.server_socket.accept()

                    self.ADDR_DB[sock_fd] = addr
                    self.READER_LIST.append(sock_fd)
                else:
                    # handle new request
                    try:
                        # self.inbox[sock.recv(self.RECV_BUFFER)] = self.ADDR_DB[sock]
                        data = sock.recv(self.RECV_BUFFER)
                        response = self.node.message.handle_message(Message(data, self.ADDR_DB[sock]))

                        if response:
                            sock.sendall(response)
                    except any:
                        # if connection is closed
                        sock.close()
                        self.READER_LIST.remove(sock)
                        del self.ADDR_DB[sock]

    # def lookForMessage(self, message):
    #     while message not in self.inbox.keys():
    #         pass
    #
    #     target_ip = self.inbox[message][0]
    #     del self.inbox[message]
    #
    #     return target_ip

    @classmethod
    def send_message(cls, server_ip, message, need_reply=False):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, SERVER_PORT))
        client_socket.sendall(message)

        if need_reply:
            reply = client_socket.recv()  # TODO: check reply if needed
            client_socket.close()
            return reply

        client_socket.close()

    # def recvMessage(self, ip):
    #     pass
