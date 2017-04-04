import socket, select
import json 

class Socket:

    def __init__ (self ,port= 12345 ,numberOfSender=4 ,IP="127.0.0.1" ,bufferSize = 4096):
        self.READER_LIST = []
        self.WRITER_LIST = []       
        self.RECV_BUFFER = bufferSize
        self.PORT = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP, self.PORT))
        self.server_socket.listen(numberOfSender)
 
        self.READER_LIST.append(self.server_socket)

        self.SOCK_ADDR_PAIR = {}

        self.inbox = {}

    def run(self):
        while True:
            read_sockets,write_sockets,error_sockets = select.select(self.READER_LIST,self.WRITER_LIST,[])
            
            for sock in write_sockets:
                pass #TODO

            for sock in read_sockets:
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.SOCK_ADDR_PAIR[sockfd] = addr
                    self.READER_LIST.append(sockfd)
                else:
                    self.inbox[sock.recv(self.RECV_BUFFER)] = self.SOCK_ADDR_PAIR[sock]


                pass #TODO


        self.server_socket.close()

    def lookForMessage(self, message):
        while message not in self.inbox.keys():
            pass

        targetip = self.inbox[message][0]
        del self.inbox[message]

        return targetip


    def addToReadList(self):
        pass

    def addToWriteList(self):
        pass

    def removeFromReadList(self):
        pass

    def removeFromWriteList(self):
        pass
