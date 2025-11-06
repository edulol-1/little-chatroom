import select
import socket
import sys
import queue

# Define the header length
# header_length = 10

# Ip address and and port number
ip_address = "127.0.0.1"
port = 10000

# Setup the socket using socket(). This will be a connection-oriented socket.
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setblocking(0)

# Bind the socket
server_sock.bind((ip_address, port))

# Listen for incomming connections
server_sock.listen(5)

# List of sockets to be monitored by selec()
socket_list = [server_sock]
messages = {}

while True:
    readable, writable, exceptional = select.select(socket_list, socket_list, socket_list)

    for sock in readable:
        # the server is available to receive new connections
        if sock is server_sock:
            conn, address = server_sock.accept()
            print(f"New connection received from {address}")
            socket_list.append(conn)
            messages[conn] = queue.Queue()
        else:
            data = sock.recv(1024)
            if data:
                for s, q in messages.items():
                    if s is sock:
                        continue
                    q.put(data)
            else:
                socket_list.remove(sock)
                sock.close()
                del messages[sock]

    for sock in writable:
        try:
            next_msg = messages[sock].get_nowait()
        except queue.Empty:
            print(f"{sys.stderr} output queue for {sock.getpeername()} is empty")
            socket_list.remove(sock)
        else:
            print(f"Sending {next_msg} to {sock.getpeername}")
            socket.send(next_msg)

    for sock in exceptional:
        if sock in socket_list:
            socket_list.remove(sock)
            sock.close()
        del messages[sock]

# Close the connection
# server_sock.shutdown(socket.SHUT_RD)
server_sock.close()
