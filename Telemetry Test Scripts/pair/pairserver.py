import zmq
import sys
import time

ctx = zmq.Context()
s = ctx.socket(zmq.PAIR)
s.bind("tcp://*:5553")

while True:
    s.send("test")
    time.sleep(1)
