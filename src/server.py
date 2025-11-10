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

while True:
    readable, _, exceptional = select.select(socket_list, [], socket_list)

    for sock in readable:
        # the server is available to receive new connections
        if sock is server_sock:
            conn, address = server_sock.accept()
            socket_list.append(conn)
            print(f"New connection received from {address}")
        else:
            data = sock.recv(1024)
            if not data:
                socket_list.remove(sock)
                sock.close()
                continue

            for s in socket_list:
                if (s is not server_sock) and (s is not sock):
                    s.send(data)

    for sock in exceptional:
        if sock in socket_list:
            socket_list.remove(sock)
            sock.close()
            print(f"Socket {sock} disconnected!")

# Close the connection
# server_sock.shutdown(socket.SHUT_RD)
server_sock.close()
