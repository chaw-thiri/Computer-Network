import socket
import threading

def setup_tcp_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1' # local host, private IP
    port = 12345

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections (max queue size is 5)
    server_socket.listen(5)
    print(f"TCP server set up and listening on {host}:{port}")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Start a new thread to handle the client
        # client_handle will assign a seperate thread or every incoming connection, thereby allowing the server to handle multiple clients simultaneously
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def handle_client(client_socket):
    # Send a greeting message to the client
    client_socket.sendall(b"Server: Hello, Client!\n")

    data = client_socket.recv(1024)
    while data:
        print(f"Received: {data.decode()}")
        data = client_socket.recv(1024)

    client_socket.close()

if __name__ == "__main__":
    setup_tcp_server()
