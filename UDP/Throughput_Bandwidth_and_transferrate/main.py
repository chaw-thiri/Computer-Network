import socket
import threading
import time

# function to calculate throughput, bandwidth, and transfer rate
def calculate_metrics(data_size, time_taken):
    throughput = data_size / time_taken
    bandwidth = data_size / time_taken
    transfer_rate = (data_size * 8) / time_taken
    return throughput, bandwidth, transfer_rate

# UDP server code
def udp_server():
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("localhost", 12345))

    while True:
        start_time = time.time()
        data, addr = server_socket.recvfrom(1024)  # port 1024 ~ 49151 are reserved for user server application
        end_time = time.time()

        latency = end_time - start_time
        throughput, bandwidth, transfer_rate = calculate_metrics(len(data), latency)

        print(f"Received {len(data)} bytes from {addr}")
        print(f"Metrics : Latency: {latency:.4f}s, Throughput: {throughput:.2f} B/s, Bandwidth: {bandwidth:.2f} B/s, TransferRate: {transfer_rate:.2f} bps")

        # echo back the data to the client
        server_socket.sendto(data, addr)

# UDP client code for file upload
def udp_upload_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Server address and port
    server_address = ("localhost", 12345)

    # Upload a file to the server
    with open("example_upload.txt", 'rb') as f:
        data = f.read(1024)
        while data:
            start_time = time.time()
            client_socket.sendto(data, server_address)
            end_time = time.time()
            latency = end_time - start_time
            print(f"Uploaded {len(data)} bytes to server")
            print(f"Upload Metrics: Latency: {latency:.4f}s")
            data = f.read(1024)

    # Close the socket after uploading the file
    client_socket.close()

# UDP client code for file download
def udp_download_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Server address and port
    server_address = ("localhost", 12345)

    # Request a file download from the server
    client_socket.sendto(b"DOWNLOAD", server_address)

    # Receive and save the downloaded file
    with open("example_download.txt", 'wb') as f:
        while True:
            data, addr = client_socket.recvfrom(1024)
            if not data:
                break
            f.write(data)

    # Close the socket after downloading the file
    client_socket.close()

# Create and start server and client threads
server_thread = threading.Thread(target=udp_server)
upload_thread = threading.Thread(target=udp_upload_client)
download_thread = threading.Thread(target=udp_download_client)

server_thread.start()
upload_thread.start()
download_thread.start()
