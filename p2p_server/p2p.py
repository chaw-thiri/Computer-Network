import socket # for tcp protocol
import threading  # for parallel tasking in python
import time # for latency measurement
import sys # for termination 

class Graph:  #  directed graph data structure to store clients as nodes
    def __init__(self):
        self.nodes = {}  # Initialize an empty dictionary to store nodes.
        #  ip addresses serves as key to identify individual hosts
        

    def add_node(self, node):
        self.nodes[node.host] = node
        

    def add_edge(self, node1, node2):
        # bidirectional connection is established to ensure both sending and receiving messages are possible
        self.nodes[node1.host].connect(node2.host, node2.port)
        self.nodes[node2.host].connect(node1.host, node1.port)
        


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # for tcp
        self.connections = []  #  to store currently active connections

    def start(self):# start a new thread
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def connect(self, peer_host, peer_port, timeout=5): # timeout 
    # connect to a peer , initiating connection
        
        try:
            connection = socket.create_connection((peer_host, peer_port), timeout=timeout)
            self.connections.append(connection)
            print(f"Connected to {peer_host}:{peer_port} ")
        except (socket.error, TimeoutError) as e:
            print(f"Connection to {peer_host}:{peer_port} failed. Error: {e}")

    def listen(self):
        # listen for a connection 
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
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
                    print(f"Sent data to {connection.getpeername()}")
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)

    def broadcast(self, data):
        # Broadcast data to all connected peers or nodes
        self.send_data(data)

    def recv_file(self, sender):
        # accept the transferred file as jpg format.
        # download the images as received_img
        with open("received_img.jpg", "wb") as file:
            while True:
                image_chunk = sender.socket.recv(2048)
                if not image_chunk:
                    break
                file.write(image_chunk)


    def send_file(self, target):
        # send image file
        file_path = "sample.jpg"  # replace the file_path with input for other files
        try:
            # read the image and send it package by package 
            with open(file_path, "rb") as file:
                for image_chunk in iter(lambda: file.read(2048), b''):
                    try:
                        target.send(image_chunk)
                    except socket.error as e:
                        print(f"Failed to send file data. Error: {e}")
                        break

        # error handling                 
        except FileNotFoundError:   # in case of other files
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading file: {e}")
        finally:
            target.close()  # Close the connection once the file is sent

    def handle_client(self, connection, address):
        while True:
            try:
                start_time = time.time() # for latency meaturement
                data = connection.recv(1024)
                if not data:
                    break
                
                print(f"Response from {address}: Received")
                print(f"Latency to {address}: {latency:.4f} seconds")
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()



if __name__ == "__main__":
    graph = Graph()
    
    node1 = Peer("127.0.0.1", 8000) # loopback ip address to test in a single machine
    node1.start()
    graph.add_node(node1)

    node2 = Peer("127.0.0.1", 8001)
    node2.start()
    graph.add_node(node2)

    node3 = Peer("127.0.0.1", 8002)
    node3.start()
    graph.add_node(node3)

    time.sleep(2)

    graph.add_edge(node1, node2)
    graph.add_edge(node2, node3)

    while True:
        print("1. Send a message")
        print("2. Broadcast a message")
        print("3. Send an image")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1': # sending unicast message 
            target_ip = input("Enter target IP address: ")
            target_port = int(input("Enter target port: "))
            target_node = graph.nodes.get((target_ip, target_port))
            message = input("Enter message: ")
            if target_node:
                node2.send_data(f"From node2: {message}", target_node.connections[0])
            else:
                print("Target not found.")

        elif choice == '2': # sending broadcast message
            message = input("Enter broadcast message: ")
            node2.broadcast(f"Broadcast from node2: {message}")

        elif choice == '3': # for file transfer
            target_ip = input("Enter target IP address: ")
            target_port = int(input("Enter target port: "))
            target_node = graph.nodes.get((target_ip, target_port))
            if target_node:
                node2.send_file(target_node)

        elif choice == '4':
            sys.exit()

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

























    

    

    


