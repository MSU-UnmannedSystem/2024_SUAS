import socket
import time

# Dronekit start
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)

# Establish connection
print("Start Camera Script")
client_socket.send("Start Camera".encode())

# Wait until camera finds target
data = client_socket.recv(1024)
print(f"Received: {data.decode()}")

client_socket.close()