import socket
import time
import random


class DataClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.server_host, self.server_port))
        print(f"Connected to {self.server_host}:{self.server_port}")

    def send_data(self):
        try:
            while True:
                data = str(random.randint(0, 100))
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                data_with_timestamp = f"{timestamp}: {data}"
                self.client_socket.send(data_with_timestamp.encode())
                time.sleep(1)
        except KeyboardInterrupt:
            print("Data sender stopped.")
        finally:
            self.client_socket.close()


if __name__ == "__main__":
    client = DataClient("127.0.0.1", 12345)
    client.connect()
    client.send_data()
