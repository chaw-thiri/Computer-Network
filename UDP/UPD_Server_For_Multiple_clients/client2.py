import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 12345)  # Replace with the server's address

while True:
    message = input("Enter a message to send to the server (or type 'exit' to quit): ")
    if message.lower() == "exit":
        break

    client_socket.sendto(message.encode(), server_address)
    data, addr = client_socket.recvfrom(1024)
    print(f"Received from server: {data.decode()}")

client_socket.close()
