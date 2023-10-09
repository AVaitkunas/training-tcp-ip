import math
import socket
import json

IP = "127.0.0.1"
PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

message = client_socket.recv(1024)
print(message.decode("utf-8"))


# client_socket.send(b"data for plotting")

def generate_sine_function_graph(num_points):
    data = {}
    for num in range(num_points):
        x = round(num * 0.1, 3)
        y = math.sin(x)
        data[x] = y
    return data


data = generate_sine_function_graph(100)
serialized_data = json.dumps(data)
client_socket.send(serialized_data.encode("utf-8"))
