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
    "psuMode" : 1,
    "throttlePercent" : 100,
    "dutyPercent" : 100,
    "pwmFrequency" : 1000,
    "rpm" : 1200.0,
    "torque" : 100.0,
    "tempC" : 30.0,
    "sourceVoltage" : 12.0,
    "pwmCurrent" : 6.0,
    "powerChange" : 1.0,
    "voltageChange" : 1.0,
    "mddStatus" : True,
    "ocpStatus" : True,
    "ovpStatus" : True,
    "timeStamp" : 0.0
}

startTimestamp = time.time()

def modifyData(data):
    data["timeStamp"] = round(time.time(), 3)
    data["psuMode"] = random.randrange(1, 2)
    data["throttlePercent"] = random.randrange(1, 100)
    data["dutyPercent"] = random.randrange(1, 100)
    data["pwmFrequency"] = random.randrange(100, 5000)
    data["rpm"] = random.uniform(1.0, 3000.0)
    data["torque"] = random.uniform(1.0, 500.0)
    data["tempC"] = random.uniform(25.0, 70.0)
    data["sourceVoltage"] = random.uniform(1.0, 40.0)
    data["pwmCurrent"] = random.uniform(1.0, 6.0)
    data["powerChange"] = random.uniform(0, 100.0)
    data["voltageChange"] = random.uniform(0, 40.0)
    data["mddStatus"] = True
    data["ocpStatus"] = True
    data["ovpStatus"] = True
    return data

def sendPubData(exit_event):
    while not exit_event.is_set():
        try:
            pub.send(msgpack.packb(modifyData(testData)))
#            logging.info(f"Sent data with timestamp - {round(time.time(), 3)}")
            time.sleep(0.1)
        except:
            traceback.print_exc()
            exit_event.set()

#

def updateSystemTime(timestamp):
    print(timestamp)
    clk_id = time.CLOCK_REALTIME
    time.clock_settime(clk_id, float(timestamp))

def sendSyncRequestSuccess():
    rep.send(msgpack.packb(True))

def receiveTimestampSync(exit_event):
    while not exit_event.is_set():
        try:
            newTimestamp = msgpack.unpackb(rep.recv())
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
