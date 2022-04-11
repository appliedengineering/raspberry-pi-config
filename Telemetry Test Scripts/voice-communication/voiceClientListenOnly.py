# Applied Engineering 2022

# imports
import chunk
import pyaudio
import threading
import socket

# vars
SERVER_IP = "192.168.1.54"  # local host
PORT = 3001  # port to run voice server on

# buffer size (bytes)
BUFFER = 256

clientSocket = None

# PyAudio vars
voiceSample = 1024  # 1024 samples
sampleFormat = pyaudio.paInt16  # 16 bit audio
channels = 1 # mono audio
fs = 44100  # 44100 samples per second (cd quality)
pa = None
recordingStream = None
outputStream = None

def establishConnectionWithServer():
    global clientSocket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((SERVER_IP, PORT))
    print("Connected to server")
    setUpVoiceWithPyAudio()

def setUpVoiceWithPyAudio():
    pa = pyaudio.PyAudio()

    global recordingStream
    global outputStream

    recordingStream = pa.open(
        format=sampleFormat,
        channels=channels,
        rate=fs,
        frames_per_buffer=voiceSample,
        input=True
    )

    outputStream = pa.open(
        format=sampleFormat,
        channels=channels,
        rate=fs,
        frames_per_buffer=voiceSample,
        output=True
    )

    print("Initialized audio devices")

    
    threading.Thread(
            target=recvServerData
            ).start()

    # send data to server
    # sendDataToServer()

def sendDataToServer():
    while True:
        recordedBuffer = recordingStream.read(BUFFER)
        clientSocket.sendall(recordedBuffer) # sendall here bc we need to make sure all data is sent

def recvServerData():
    while True:
        dataToBePlayed = clientSocket.recv(BUFFER)
        outputStream.write(dataToBePlayed)

establishConnectionWithServer()