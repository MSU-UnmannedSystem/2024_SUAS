import socket

# Client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)

client_socket.send("Start Camera".encode())
data = client_socket.recv(1024)
print(f"Received: {data.decode()}")

client_socket.close()