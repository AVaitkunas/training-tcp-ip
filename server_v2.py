import json
import socket

IP = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP, PORT))
server_socket.listen(1)

print(f"Serving on {IP}:{PORT}")

client_socket, client_address = server_socket.accept()

# send message
msg = "Hello from server!"
client_socket.send(msg.encode("utf-8"))

# receive message
received = client_socket.recv(1024*5)
print(received.decode("utf-8"))

# decode message and plot

decoded = received.decode("utf-8")
print(decoded)
decoded_object = json.loads(decoded)
print(type(decoded_object))


# plot graph
import matplotlib.pylab as plt



x = decoded_object.keys()
y= decoded_object.values()

plt.plot(x, y)
plt.show()