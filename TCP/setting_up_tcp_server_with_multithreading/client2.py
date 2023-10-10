import socket

def main():
    host = "127.0.0.1"  # Replace with the server's IP address or hostname
    port = 12345        # Replace with the server's port number

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        # Receive and display the server's greeting message
        data = client_socket.recv(1024)
        print(f"Server says: {data.decode()}")

        while True:
            message = input("Enter a message to send to the server (or type 'exit' to quit): ")
            if message.lower() == "exit":
                break

            # Send the message to the server
            client_socket.sendall(message.encode())

            # Receive and display the server's response
            data = client_socket.recv(1024)
            print(f"Server response: {data.decode()}")

    except ConnectionRefusedError:
        print("Connection to the server refused. Ensure the server is running and the address is correct.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
