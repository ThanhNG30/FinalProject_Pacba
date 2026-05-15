from socket import *

client = socket(AF_INET, SOCK_STREAM)
host = "192.168.50.100"
port = 5150
client.connect((host, port))

print("Conected to server:")

while True:
    text = input("Enter message: ")
    data = text.encode()
    client.send(data)
    if text == "exit":
        break

client.close()
