# UDP Server with Latency Calculation

* This Python script demonstrates a simple UDP server that receives data from clients, calculates the latency, and echoes the data back to the client. It uses the User Datagram Protocol (UDP) for communication.
 

### Code Explanation

* udp_server.py: Implements the UDP server that listens for incoming data packets, calculates latency, and echoes the data back to the client.
* handle_client(): A function to handle incoming data, calculate latency, and send the data back to the client.
* The server uses multithreading to handle multiple clients concurrently.
