import socket

IP = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP, PORT))
server_socket.listen(1)

print(f"Serving on {IP}:{PORT}")

client_socket, client_address = server_socket.accept()
msg = "Hello from server!"
client_socket.send(msg.encode("utf-8"))
