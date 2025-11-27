import socket
import sys
import errno
import threading

class ClientSocket:
    def __init__(self, server_ip="127.0.0.1", server_port=10000):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_sock.connect((self.server_ip, self.server_port))

    def receive_message(self):
        data = self.client_sock.recv(1024)
        if len(data) == 0:
            raise IOError("Connection closed by server!")

        received_message = data.decode("utf-8")
        return received_message

    def send_message(self, message):
        if message != "" and message is not None:
            message = message.encode("utf-8")
            self.client_sock.send(message)

    def close(self):
        self.client_sock.close()
