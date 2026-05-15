from socket import *

client = socket(AF_INET, SOCK_STREAM)
host = "192.168.50.100"
port = 5150
# Function for connection
def connect():
    client.connect((host, port))
    print("Conected to server:")
# Function to run the cleint loop.
def run(text):
    if text == "caught":
        ghosts_caught = True
    elif text == "not caught":
        ghosts_caught = False
    if text == "exit":
        break
            
    # convert string to bytes
    data = text.encode()
    # send encode message to the server
    client.send(data)
    # wait for response
    response = client.recv(1024).decode()
    # print server response
    print(response)
       
client.close()
