# UDP use Datagram protocol
import socket                       # for network communication
import threading                    # for multithreading


# create a UDP socket 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "localhost"
port = 12345 
server_socket.bind((host, port))   # bind the socket to local host on port 12345

def handle_client(client_socket,client_address):
    """handle the incoming data and echo it back to the client + latency calculation"""
    data, addr = client_socket.recvfrom(1024)   # port 1024 ~49151 are reserved for user server application
    print(f"Received {data} from {addr}")
    # send data back to the client
    client_socket.sendto(data,addr)

# main function to handle incoming connections (handle multiple clients using threading)
def main():
    while True:
        data, addr = server_socket.recvfrom(1024)
        # start a new thread to handle the client communication
        threading.Thread(target=handle_client, args=(server_socket,addr)).start()

if __name__ == "__main__":
    main()
