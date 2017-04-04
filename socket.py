import socket, select
import json


class Socket:
    def __init__(self, port=12345, numberOfSender=4, IP="127.0.0.1", bufferSize=4096):
        self.READER_LIST = []
        self.WRITER_LIST = []
        self.RECV_BUFFER = bufferSize
        self.PORT = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP, self.PORT))
        self.server_socket.listen(numberOfSender)

        self.READER_LIST.append(server_socket)
