from socket import *

client = socket(AF_INET, SOCK_STREAM)
host = "192.168.50.100"
port = 5150
# Function for connection
def connect():
    client.connect((host, port))
    print("Conected to server:")
# Function to run the cleint loop.
def run(pacba_is_caught):
    msg = ""
    if pacba_is_caught:
        msg = "caught"
    else:
        msg = "not caught"
            
    # convert string to bytes
    data = str.encode()
    # send encode message to the server
    cserver.send(data)
    if text == "exit":
        break
client.close()
