import sys
import errno
import threading
from interface_handler import InterfaceHandler
from client_socket import ClientSocket
from queue import Queue

class Chatroom:
    def __init__(self):
        self.client_sock = ClientSocket()
        self.interface = InterfaceHandler()
        self.commands = Queue()
        self.exit_f = Queue()

    def start(self):
        self.client_sock.connect()
        self.interface.launch_interface()

    def close(self):
        self.client_sock.close()
        self.interface.close()

    def receive_messages(self):
        while not exit_f.empty():
            message = self.client_sock.receive_message()
            self.commands.put((print_message, message))

    def send_and_print_messages(self):
        while True:
            while not self.incoming_messages.empty():
                self.interface.print_message(self.incoming_messages.get())
            message = self.interface.type_and_get_message()
            #asyncio?
