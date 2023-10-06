import socket

def setup_tcp_client(client_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345

    try:
        client_socket.connect((host, port))
        print(f"Client {client_id} connected to {host}:{port}")

        # Send a message to the server
        message = f"Client {client_id}: Hello, Server!"
        client_socket.sendall(message.encode())

        # Receive and print the server's response
        data = client_socket.recv(1024)
        print(f"Received: {data.decode()}")

    except Exception as e:
        print(f"Client {client_id} error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Start multiple clients (adjust the range as needed)
    for i in range(5):
        setup_tcp_client(i)
