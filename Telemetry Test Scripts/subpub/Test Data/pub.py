# Telemetry ZeroMQ TCP Publisher
# Copyright (c) 2022 Applied Engineering

import concurrent.futures
import logging
import msgpack
import queue
import threading
import traceback
import zmq
import time
import random

# Set logging verbosity.
# CRITICAL will not log anything.
# ERROR will only log exceptions.
# INFO will log more information.
log_level = logging.INFO

# ZeroMQ Context.
context = zmq.Context.instance()
# Define the pub socket using the Context.
pub = context.socket(zmq.PUB)
pub.bind("tcp://*:5556")

# Define the rep socket using the Context.
rep = context.socket(zmq.REP)
rep.bind("tcp://*:55561")

# Define message end sequence.
end = b'EOM\n'

testData = {
    "TP" : 35, # Throttle Percent
    "DP" : 150, # Duty Percent
    "CP" : 30.0, # Chip Temp (float)
    "BV" : 24.0, # Battery Voltage
    "UV" : True, # Undervolt Protection
    "SM" : True, # Solar Mode
    "EN" : True, # Motor Enabled
    "BC" : 15.0, # Battery Current
    ## end motor control data
    "posLat" : 38.335196,
    "posLon" : -121.092967,
    "speed" : 13.2, # Speed of boat measured from gps m/s
    "timeStamp" : 0.0
}

startTimestamp = time.time()

def modifyData(data):
    data["timeStamp"] = round(time.time(), 3)
    data["TP"] = random.randrange(1, 100)
    data["DP"] = random.randrange(1, 180)
    data["CP"] = random.uniform(25.0, 70.0)
    data["BV"] = random.uniform(20.0, 30.0)
    data["UV"] = True
    data["SM"] = True
    data["EN"] = True
    data["BC"] = random.uniform(0, 40.0)
    data["posLat"] = 38.335 + random.uniform(0, 0.00099)
    data["posLon"] = -121.092 + random.uniform(0, 0.00099)
    data["speed"] = random.uniform(0.0, 25.0)
    return data

def sendPubData(exit_event):
    while not exit_event.is_set():
        try:
            d = msgpack.packb(modifyData(testData))
            print(d)
            pub.send(d)
            logging.info(f"Sent data with timestamp - {round(time.time(), 3)}")
            time.sleep(0.1)
        except:
            traceback.print_exc()
            exit_event.set()

#

def updateSystemTime(timestamp):
    #print(timestamp)
    clk_id = time.CLOCK_REALTIME
    time.clock_settime(clk_id, float(timestamp))

def sendSyncRequestSuccess():
    rep.send(msgpack.packb(True))

def receiveTimestampSync(exit_event):
    while not exit_event.is_set():
        try:
            newTimestamp = msgpack.unpackb(rep.recv(flags=zmq.NOBLOCK))
            logging.info(f"Updating timestamp with {newTimestamp}")
            updateSystemTime(newTimestamp)
            sendSyncRequestSuccess()
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                logging.info("No timestamp update message")
                pass    # no message ready yet
            else:
                traceback.print_exc()
        except:
            traceback.print_exc()
            exit_event.set()
        time.sleep(1)

if __name__ == '__main__':
    try:
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=log_level, datefmt="%H:%M:%S")
        # Create exit event
        exit_event = threading.Event()
        # Spawn worker threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(sendPubData, exit_event)
            executor.submit(receiveTimestampSync, exit_event)
    except KeyboardInterrupt:
        logging.info('Setting exit event.')
        exit_event.set()
    except:
        traceback.print_exc()
        exit_event.set()
