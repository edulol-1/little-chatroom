import socket
import sys
import errno

# Establish the server and port and address
server_ip = "127.0.0.1"
server_port = 10000

# Create a new socket for a TCP connection
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client to the server
client_sock.connect((server_ip, server_port))

# Set the socket to be non-blocking
client_sock.setblocking(False)

# Loop to send continuous requests:
while True:
    message = input("> ")

    if message:
        print(message)
        message = message.encode("utf-8")
        client_sock.send(message)

    while True:
        try:
            data = client_sock.recv(1024)
        except IOError as e:
            print(f"Reading error {str(e)}")
            break
        else:
            if len(data) == 0:
                print("Connection closed by the server")
                client_sock.close()
                sys.exit()

            received_message = data.decode("utf-8")
        print(f"other > {received_message}")



