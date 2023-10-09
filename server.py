import socket
import re
import matplotlib.pyplot as plt
from collections import deque


class DataServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data_history = deque(maxlen=50)
        self.pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}): (\d+)"
        self.setup_plot()

    def setup_plot(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.set_title("Real-Time Data Plot")

    def handle_client(self, client_socket):
        addr = client_socket.getpeername()
        print(f"Accepted connection from {addr}")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            data = data.decode()
            match = re.search(self.pattern, data)
            if match:
                timestamp, value = match.groups()
                self.data_history.append((timestamp, int(value)))
                self.update_plot()

        print(f"Connection from {addr} closed.")
        client_socket.close()

    def update_plot(self):
        timestamps, values = zip(*self.data_history)
        self.line.set_data(range(len(self.data_history)), values)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.flush_events()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            self.handle_client(client_socket)


if __name__ == "__main__":
    server = DataServer("127.0.0.1", 12345)
    server.start()
