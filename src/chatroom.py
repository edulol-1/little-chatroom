import sys
import errno
import threading
import curses
from interface_handler import InterfaceHandler
from client_socket import ClientSocket
from queue import Queue
from queue import Empty

class Chatroom:
    def __init__(self):
        self.client_sock = ClientSocket()
        self.interface = InterfaceHandler()
        self.messages_q = Queue()
        self.exit_f = Queue()
        self.username = ""

    def set_username(self, username):
        self.username = username

    def start(self):
        self.client_sock.connect()
        self.client_sock.send_message(self.username)
        self.interface.launch_interface()

    def close(self):
        self.client_sock.close()
        self.interface.close()

    def receive_messages(self):
        while self.exit_f.empty():
            try:
                message = self.client_sock.receive_message()
            except IOError:
                message = "Connection close by the server!"
                self.interface.print_message(message)
                self.exit_f.put(1)

            self.messages_q.put(message)

    def send_and_print_messages(self):
        input_buff = ""
        while self.exit_f.empty():
            while not self.messages_q.empty():
                try:
                    self.interface.print_message(self.messages_q.get_nowait())
                except Empty:
                    pass

            ch = self.interface.type_and_get_ch()
            if ch == -1:
                continue

            if ch in (10, 13):
                if input_buff.lstrip() == "exit":
                    self.exit_f.put(1)
                    break
                self.interface.print_message(input_buff)
                self.client_sock.send_message(input_buff)
                input_buff = ""
                self.interface.clear_chat_win()
            elif ch in (curses.KEY_BACKSPACE, 8, 127):
                input_buff = input_buff[:-1]
                self.interface.clear_chat_win()
                self.interface.buffer_to_chat(input_buff)
            else:
                input_buff += chr(ch)
                self.interface.buffer_to_chat(input_buff)

if __name__ == "__main__":
    username = input("Introduce your username: ")
    while len(username) > 10:
        username = input("It must be 10 characters top!: ")

    chatroom = Chatroom()
    chatroom.set_username(username)
    try:
        chatroom.start()
        t_recv = threading.Thread(target=chatroom.receive_messages, daemon=True)
        t_recv.start()
        chatroom.send_and_print_messages()
    except KeyboardInterrupt:
        print("See you soon!")
        print("Connection closed by server!")
    except Exception as e:
        print(f"{e}")
    finally:
        chatroom.close()
