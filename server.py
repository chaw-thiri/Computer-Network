import socket
import threading
import base64 # for sending images 
import time

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

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
    def broadcast(self,data):
        self.send_date(data)

    def send_data(self, data, target=None, is_image=False):
        for connection in self.connections:
            try:
                if target is None or connection == target:
                    if is_image:
                        connection.sendall(base64.b64encode(data))
                    else:
                        connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                if data.startswith(b"image:"):
                    image_data = base64.b64decode(data[len("image:"):])
                    # Handle the image_data as needed, e.g., save to a file or process it
                    print(f"Received image from {address}")
                else:
                    print(f"Received data from {address}: {data.decode()}")
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

    node2.connect("127.0.0.1", 8000) # work
    time.sleep(1)  # Allow connection to establish


    node2.connect("127.0.0.1",8002)# works
    time.sleep(1)
    
    


    while True:
        print("1. Send a message")
        print("2. Send an image")
        print("3. Broadcast a message")
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
            image_path = input("Enter the path to the image file: ")
            try:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                    node2.send_data(b"image:" + image_data, is_image=True)
            except FileNotFoundError:
                print("Image file not found.")

        elif choice == '3':
            message = input("Enter broadcast message: ")
            node2.broadcast(f"Broadcast from node2: {message}")

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
