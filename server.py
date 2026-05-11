from socket import *
# server socket
server = socket(AF_INET, SOCK_STREAM)
host = ""
port = 5150
# bind server
server.bind((host, port))

print("Waiting client...")
server.listen(5)
# Accept connection
(client, addr) = server.accept()
print("Client accepted from: ", addr)
# variable to track the ghost status
ghosts_caught = False

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

client.close()
server.close()
print("Server exited.")
