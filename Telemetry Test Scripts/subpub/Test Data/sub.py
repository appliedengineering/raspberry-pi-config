# Telemetry ZeroMQ TCP Subscriber
# Copyright (c) 2022 Applied Engineering

import logging
import msgpack
import traceback
import zmq
import time

# Set logging verbosity.
# CRITICAL will not log anything.
# ERROR will only log exceptions.
# INFO will log more information.
log_level = logging.INFO

# ZeroMQ setup
ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)

address = "tcp://raspberrypi.local:5556"

sub.connect(address) # change localhost to the IP of the other computer
sub.subscribe("") # Subscribe to all topics

if __name__ == '__main__':
    try:
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=log_level, datefmt="%H:%M:%S")
        logging.info('Listening for data from %s.', address)
        while True:
            try:
                print(msgpack.unpackb(sub.recv(copy=False, flags=zmq.NOBLOCK)))
                logging.info('Received data.')
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    pass    # no message ready yet
                else:
                    traceback.print_exc()
            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info('Exiting now.')
        sub.close()
    except:
        traceback.print_exc()
