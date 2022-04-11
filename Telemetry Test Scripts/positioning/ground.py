import zmq
import time
import msgpack

# env vars
transmitPort = 5552
receivePort = 5551
receiveIP = "localhost"

testData = [34.147518,-118.051535]

###

ctx = zmq.Context()

pub = ctx.socket(zmq.PUB)
sub = ctx.socket(zmq.SUB)

pub.bind("tcp://*:" + str(transmitPort))
sub.connect("tcp://" + str(receiveIP) + ":" + str(receivePort))
sub.subscribe("")

try:
   while True:
      pub.send(msgpack.packb(testData))
      print(f"sent data - {testData}")

      try:
         print(msgpack.unpackb(sub.recv(copy=False, flags=zmq.NOBLOCK)))
      except zmq.ZMQError as e:
         if e.errno == zmq.EAGAIN:
             print("no msg")
             pass
         else:
             print(e)

      time.sleep(0.1)
except KeyboardInterrupt:
   print("exiting")

##

pub.close()
sub.close()
ctx.term()



