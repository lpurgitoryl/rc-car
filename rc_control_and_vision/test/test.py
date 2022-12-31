import socket
server = socket.socket() 
server.bind(("192.168.183.1", 6677)) 
server.listen(4) 
client_socket, client_address = server.accept()
print(client_address, "has connected")
while True:
    recvieved_data = client_socket.recv(1024)
    print(recvieved_data)