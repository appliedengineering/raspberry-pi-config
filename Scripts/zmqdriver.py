import zmq
import msgpack
import time

class zmqdriver: # for gps positioning communication
    __ctx = zmq.Context()

    __pub = __ctx.socket(zmq.PUB)
    __sub = __ctx.socket(zmq.SUB)
    
    __transmitPort = 5551
    __receivePort = 5552
    __receiveIP = "localhost"

    def __init__(self, groundIP):
        self.__receiveIP = groundIP

        self.__pub.bind("tcp://*:" + str(self.__transmitPort))
        self.__sub.connect("tcp://" + str(self.__receiveIP) + ":" + str(self.__receivePort))
        self.__sub.subscribe("")

    def transmitPosition(self, lat, lon):
        print(lat, lon)
        self.__pub.send(msgpack.packb([lat, lon]))

    def receivePosition(self):
        d = []
        try:
            d = msgpack.unpackb(self.__sub.recv(copy=False, flags=zmq.NOBLOCK))
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                pass
            else:
                print(e)
        return d