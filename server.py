import socket
import threading
from collections import namedtuple
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt

point_data = namedtuple("point_data", ("x", "y"))


@dataclass
class PlotData:
    values: List[point_data]


class ServerPlot:
    """object for plotting"""

    plot_data_buffer = None

    def __init__(self):
        # this will store data for each of the client
        self.client_plots = {}

        # start plotting thread
        self.lock = threading.Lock()
        self.start_plotting_thread()

    def start_plotting_thread(self):
        plot_thread = threading.Thread(target=self.update_plot_thread)
        plot_thread.daemon = True
        plot_thread.start()

    def add_client(self, client_address):
        self.client_plots[client_address] = PlotData([])

    def process_data(self, client_address, data):
        try:
            y_value = float(data.decode("utf-8"))
            with self.lock:
                client_plot_data = self.client_plots[client_address]
                x_value = len(client_plot_data.values) if client_plot_data.values is not None else 0
                point = point_data(x=x_value, y=y_value)
                client_plot_data.values.append(point)

                self.plot_data_buffer = self.client_plots.copy()
        except ValueError:
            print(f"Invalid data received from {client_address}")

    def update_plot_thread(self):
        while True:
            if self.plot_data_buffer:
                # Clear the current plot
                plt.clf()
                with self.lock:
                    # iterate over your clients and it's data
                    for client_address, data in self.plot_data_buffer.items():
                        x_values = [item.x for item in data.values]
                        y_values = [item.y for item in data.values]
                        plt.plot(x_values, y_values, label=f"Client {client_address}")

                plt.xlabel("X")
                plt.ylabel("Y")
                plt.legend()
                plt.draw()
                self.plot_data_buffer = None

            # pause for graph to be updated
            plt.pause(0.1)


class MultiPlotServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_plot = ServerPlot()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"New client: {client_address}")

                # Create a client plot
                self.server_plot.add_client(client_address)
                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_socket, client_address)
                )
                client_thread.start()

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                self.server_plot.process_data(client_address, data)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 12345
    multi_plot_server = MultiPlotServer(host, port)
    multi_plot_server.start_server()
