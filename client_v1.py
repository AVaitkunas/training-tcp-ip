import socket
IP = "127.0.0.1"
PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

message = client_socket.recv(1024)
print(message.decode("utf-8"))
