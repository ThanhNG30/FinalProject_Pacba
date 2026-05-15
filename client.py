from socket import *

client = socket(AF_INET, SOCK_STREAM)
host = "192.168.50.100"
port = 5150
# Function for connection
def connect():
    client.connect((host, port))
    print("Conected to server:")
# Function to run the cleint loop.
def run(caught):
        # asks user for input
        text = input("Enter message: ")
        # convert string to bytes
        data = text.encode()
        # send encode message to the server
        client.send(data)
        # wait for response
        response = client.recv(1024).decode()
        # print server response
        print(response)
        if text == "exit":
            break

client.close()
