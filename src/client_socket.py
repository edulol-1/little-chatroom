import socket
import sys
import errno
import threading
import select

class ClientSocket:
    def __init__(self):
        self.server_ip = ""
        self.server_port = ""
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_ip="127.0.0.1", server_port=10000):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_sock.connect((self.server_ip, self.server_port))
        self.client_sock.setblocking(0)

    def receive_message(self):
        message = ""
        while True:
            try:
                message = self.client_sock.recv(1024)
                break
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    continue
        if len(message) == 0:
            raise IOError("Connection closed by server!")
        return message.decode("utf-8")

    def send_message(self, message):
        total_sent = 0
        message = message.encode("utf-8")
        while len(message):
            try:
                sent = self.client_sock.send(message)
                total_sent += sent
                message = message[sent:]
            except socket.error as e:
                if e.errno != errno.EAGAIN:
                    raise e
                select.select([], [self.client_sock], [])

    def close(self):
        self.client_sock.close()
