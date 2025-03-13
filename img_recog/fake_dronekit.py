import socket
import time

def connect():
	# Dronekit start
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', 12345)
	client_socket.connect(server_address)

	# Establish connection
	print("Start Camera Script")
	client_socket.send("Start Camera".encode())

	# Wait until camera finds target
	data = client_socket.recv(1024)
	print("Received: {}".format(data.decode()))

	client_socket.close()

try:
	connect()
except:
	print("End by Camera Script")
