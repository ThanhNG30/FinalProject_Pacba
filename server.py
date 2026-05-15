from socket import *

# server socket
server = socket(AF_INET, SOCK_STREAM)
host = ""
port = 5150
# bind server
server.bind((host, port))
server.listen(5)
# List to track the connected clients
clients = []
ghosts_caught = False # variable 
# Function client connection.
def init_server(numClients):
    print("Waiting for client...")
    while len(clients) < numClients:
        # Accept connection
        (client, addr) = server.accept()
        print("Client accepted from: ", addr)
        # Store client
        clients.append(client)
        
# Function update server        
def update_server():
    global ghosts_caught
    for client in clients:
        
    #while True:
        # recived data 
        data = client.recv(1024)
        # check for data 
        if not data:
            clients.remove(client)
            client.close()
            continue
        # process data, converts bytes to string.
        text = data.decode()
        print("data:", text)
        # Logic
        if text == "caught":
            ghosts_caught = True
        elif text == "not caught":
            ghosts_caught = False
        elif text == "exit":
            clients.remove(client)
            client.close()
            continue

def shutdown_server():
    # close all connections
    for client in clients:
        client.close()
    server.close()
    print("Server exited.")
