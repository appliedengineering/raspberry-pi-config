# Applied Engineering 2022

# imports
import socket
import threading
import concurrent.futures
import sys

# vars
SERVER_IP = "localhost"  # local host

PORT = 3001  # port to run voice server on

# buffer size (bytes)
BUFFER = 256

serverSocket = 0
clientsSockets = []

def startServerOperations():
    print("Starting voice server:")
    print("HOSTNAME: " + socket.gethostname())
    # create an ipv4 socket with tcp
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((SERVER_IP, PORT))

    startAcceptingConnections(serverSocket)

def startAcceptingConnections(serverSocket):
    print("Server ready!")
    serverSocket.listen(5) # allow 5 unaccepted connections for backlog

    try:
        while True:
            clientSocket, address = serverSocket.accept()

            clientsSockets.append(clientSocket)
        
            print("New client connected")

            # # start new thread for client
            # thread = threading.Thread(
            #     target=handleClientSocket,
            #     args=((clientSocket, address))
            #     )
            # thread.setDaemon = True

            # thread.start()
    except KeyboardInterrupt:
        sys.exit()

def handleClientSocket(clientSocket, address):
    while True:
            try:
                incomingVoiceData = clientSocket.recv(BUFFER)
                broadcastClientData(clientSocket, incomingVoiceData, address)
            
            except socket.error:
                clientSocket.close()
                clientsSockets.remove(clientSocket)

def broadcastClientData(sourceSock, data, address):
    for clientSocket in clientsSockets:
        # don't forward voice data to self
        if clientSocket != serverSocket and clientSocket != sourceSock:
            clientSocket.send(data) # dont use sendAll, we don't want to resend old data


if __name__=="__main__":
    startServerOperations()
