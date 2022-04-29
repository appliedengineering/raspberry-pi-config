import zmq
import time
import msgpack

ctx = zmq.Context()
s = ctx.socket(zmq.PAIR)
#s.setsockopt(zmq.CONFLATE, 1)
s.connect("tcp://localhost:5553")

while True:
    print(msgpack.unpackb(s.recv()))
    time.sleep(0.1)
