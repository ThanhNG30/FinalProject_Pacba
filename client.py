from socket import *

server = socket(AF_INET, SOCK_STREAM)
host = "192.168.50.122"
port = 5150
# Function for connection
def connect():
    server.connect((host, port))
    print("Conected to server:")
# Function to run the cleint loop.

# Expect a bool
def run(pacba_is_caught):
    msg = ""
    if pacba_is_caught:
        msg = "caught"
    else:
        msg = "not caught"
            
    # convert string to bytes
    data = str.encode(msg)
    # send encode message to the server
    server.send(data)
    
def close():
    server.close()
