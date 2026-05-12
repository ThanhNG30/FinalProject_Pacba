from socket import *
import threading

# server socket
server = socket(AF_INET, SOCK_STREAM)
host = ""
port = 5150
# bind server
server.bind((host, port))
server.listen(5)

clients = []
ghosts_caught = False

def init_server():
    
    print("Waiting client...")
    while True:
        # Accept connection
        (client, addr) = server.accept()
        print("Client accepted from: ", addr)
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,)).start()
        
def update_server():
    global ghosts_caughts
    while True:
        # recived data 
        data = client.recv(1024)
        # check for data 
        if not data:
            break
        # process data, converts bytes to string.
        text = data.decode()
        print("data:", text)
        # Logic 
        if text == "caught":
            ghosts_caught = True
        elif text == "not caught":
            ghosts_caught = False
        elif text == "exit":
            break
    print("Ghosts caught:", ghosts_caught)
    clients.remove(client)
    client.close()
    
def shutdown_server():
    for client in clients:
    client.close()
    server.close()
    print("Server exited.")
