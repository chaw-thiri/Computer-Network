## TCP Server with Multi-threading
The key difference from simple TCP server is that in this server for each accepted client connection, a new thread (client_handler) is created to handle that specific client's communication. This allows the server to handle multiple clients simultaneously.

With this modification, each client that connects to the server will be processed in a separate thread, allowing for concurrent communication.

## Server testing 
# View from client 1
![image](https://github.com/chaw-thiri/Computer-Network/assets/113085742/0fb2a06a-6da6-4482-97d1-7bc118617418)

# View from client 2 
![image](https://github.com/chaw-thiri/Computer-Network/assets/113085742/1be1c14d-62bc-4220-bc70-cfde89901bef)




# View from server
![image](https://github.com/chaw-thiri/Computer-Network/assets/113085742/02c9d386-ab13-42b4-b5de-afed7f684efb)


