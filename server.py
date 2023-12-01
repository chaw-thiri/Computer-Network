import socket
import threading
import os

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.threads = []  # for os

    def connect(self, peer_host, peer_port):
        connection = socket.create_connection((peer_host, peer_port))
        self.connections.append(connection)
        print(f"Connected to {peer_host}:{peer_port}")

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
        connections_to_remove = []

        for connection in self.connections:
            try:
                if target is None or connection == target:
                    connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                connections_to_remove.append(connection)

        self.connections = [conn for conn in self.connections if conn not in connections_to_remove]

    def broadcast(self, data):
        self.send_data(data)

    def handle_client(self, connection, address):
        file_path = "received_img.jpg"

        with open(file_path, "wb") as file:
            while True:
                try:
                    data = connection.recv(2048)
                    if not data:
                        break
                    file.write(data)
                except socket.error:
                    break

        print(f"File received from {address}. Saved as {file_path}")
        self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        self.threads.append(listen_thread)
        listen_thread.start()

    def recv_file(self, sender):
        with open("received_img.jpg", "wb") as file:
            while True:
                image_chunk = sender.socket.recv(2048)
                if not image_chunk:
                    break
                file.write(image_chunk)

    def send_file(self, target):
        file_path = "snow.jpg"
        try:
            with open(file_path, "rb") as file:
                for image_chunk in iter(lambda: file.read(2048), b''):
                    try:
                        target.send(image_chunk)
                    except socket.error as e:
                        print(f"Failed to send file data. Error: {e}")
                        break
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading file: {e}")
        finally:
            target.close()  # Close the connection once the file is sent

# Example usage:
if __name__ == "__main__":
    node1 = Peer("0.0.0.0", 8000)
    node1.start()

    node2 = Peer("0.0.0.0", 8001)
    node2.start()

    node3 = Peer("0.0.0.0", 8002)
    node3.start()

    # Give some time for nodes to start listening
    import time
    time.sleep(2)

    node2.connect("127.0.0.1", 8000)
    node2.connect("127.0.0.1", 8002)
    loop = 1
    while loop:
        counter = 1 
        while(counter): 
            time.sleep(3)
            counter = 0

        print("1. Send a message")
        print("2. Broadcast a message")
        print("3. Send an image")
        print("4. Exit")
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
            target_ip = input("Enter target IP address: ")
            target_port = int(input("Enter target port: "))
            target = next((conn for conn in node2.connections if conn.getpeername() == (target_ip, target_port)), None)
            node2.send_file(target)

        elif choice == '4':
            print("Exiting the program")
            
            os._exit(0)

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
