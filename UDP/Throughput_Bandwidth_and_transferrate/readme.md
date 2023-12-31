# UDP File Transfer and Metrics Calculation

This Python script demonstrates UDP file transfer between a client and a server, along with the calculation of various network metrics such as latency, throughput, bandwidth, and transfer rate. It uses the UDP (User Datagram Protocol) for communication.   

## Latency 
* The difference in time before and after receiving data.

## Throughput 
* Throughput = total data sent / total time taken

## Bandwidth
* Maximum rate of data transfer through a given path.    
* Bandwidth = total data sent / total time taken            (same as throughput)

## Transfer rate
* Transfer rate = total data sent * 8 / total time taken    (bytes to bits) 
## Code explanation 

* udp_server(): Implements the UDP server that listens for incoming data packets, calculates network metrics, and echoes the data back to the client.
* udp_client(): Provides UDP clients for file upload and download. The upload client reads a file and sends it to the server in chunks, while the download client requests and saves a file received from the server.
* calculate_metrics(): A function to calculate network metrics based on data size and time taken.
* udp_upload_client(): Uploads a file to the server and displays upload metrics.
* udp_download_client(): Downloads a file from the server.
* Threads are used to run the server, upload client, and download client concurrently.
