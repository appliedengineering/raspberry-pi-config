import zmq
import time

ctx = zmq.Context()
sock = ctx.socket(zmq.SUB)
sock.connect("tcp://localhost:5556") # change localhost to the IP of the other computer
sock.subscribe("") # Subscribe to all topics

print("Starting receiver loop ...")
while True:
    msg = sock.recv_string()
    print("Received string: %s ..." % msg)

sock.close()
ctx.term()
