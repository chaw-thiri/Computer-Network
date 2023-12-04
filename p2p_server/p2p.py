import socket
import threading
import time

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def connect(self, peer_host, peer_port, timeout=5):
        start_time = time.time()
        try:
            connection = socket.create_connection((peer_host, peer_port), timeout=timeout)
            self.connections.append(connection)
            print(f"Connected to {peer_host}:{peer_port} in {time.time() - start_time:.4f} seconds")
        except (socket.error, TimeoutError) as e:
            print(f"Connection to {peer_host}:{peer_port} failed. Error: {e}")

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address}")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_data(self, data, target=None):
        for connection in self.connections:
            try:
                if target is None or connection == target:
                    start_time = time.time()
                    connection.sendall(data.encode())
                    print(f"Sent data to {connection.getpeername()} in {time.time() - start_time:.4f} seconds")
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)

    def broadcast(self, data):
        self.send_data(data)

    def handle_client(self, connection, address):
        while True:
            try:
                start_time = time.time()
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Received data from {address}: {data.decode()} in {time.time() - start_time:.4f} seconds")
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

# Example usage:
if __name__ == "__main__":
    node1 = Peer("0.0.0.0", 8000)
    node1.start()

    node2 = Peer("0.0.0.0", 8001)
    node2.start()

    node3 = Peer("0.0.0.0", 8002)
    node3.start()

    # Give some time for nodes to start listening
    time.sleep(2)

    node2.connect("127.0.0.1", 8000)
    time.sleep(1)  # Allow connection to establish

    node2.connect("127.0.0.1", 8002)  # works
    time.sleep(1)

    while True:
        print("1. Send a message")
        print("2. Broadcast a message")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            target_ip = input("Enter target IP address: ")
            target_port = int(input("Enter target port: "))
            target = next((conn for conn in node2.connections if conn.getpeername() == (target_ip, target_port)), None)
            message = input("Enter message: ")
            if target:
                node2.send_data(f"From node2: {message}", target)
            else:
                print("Target not found.")

        elif choice == '2':
            message = input("Enter broadcast message: ")
            node2.broadcast(f"Broadcast from node2: {message}")

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
