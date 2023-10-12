import math
import socket
import random
import time


class PlotClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.client_socket.connect((self.server_host, self.server_port))
        print("Connected to the server")

    def send_sine_func(self):
        number = 0
        while True:
            y = math.sin(number)
            data = str(y).encode("utf-8")
            self.client_socket.send(data)
            print(f"Sent data to the server: {data.decode('utf-8')}")
            time.sleep(1)
            number += 1

    def send_random_data(self):
        while True:
            data = str(random.uniform(0, 10)).encode("utf-8")
            self.client_socket.send(data)
            print(f"Sent data to the server: {data.decode('utf-8')}")
            time.sleep(1)  # Adjust the interval as needed

    def close_connection(self):
        self.client_socket.close()


if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 12345

    plot_client = PlotClient(server_host, server_port)
    plot_client.connect_to_server()
    try:
        plot_client.send_sine_func()
        # plot_client.send_random_data()
    except KeyboardInterrupt:
        print("Client terminated by user")
    finally:
        plot_client.close_connection()
