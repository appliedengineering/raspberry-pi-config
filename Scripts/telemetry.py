
# Telemetry ZeroMQ Transmitter
# Copyright (c) 2020 Applied Engineering

import concurrent.futures
import logging
import msgpack
import queue
import serial
#import serial.tools.list_ports
import threading
import traceback
import zmq
import time

import motorcontrollerdriver
import gpsdriver
from alignmentcalc import alignmentcalc

#
motorctrl = motorcontrollerdriver.motorcontrollerdriver("/dev/ttyUSB1", 115200)
gps = gpsdriver.gpsdriver("/dev/serial0", 115200)


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

# Define the pair socket using the Context.
pair = context.socket(zmq.PAIR)
pair.connect("tcp://localhost:5553")

# Define message end sequence.
end = b'EOM\n'

previousBoatCoordinates = []
previousBoatTimestamp = 0.0

def updateSystemTime(timestamp):
    #print(timestamp)
    clk_id = time.CLOCK_REALTIME
    time.clock_settime(clk_id, float(timestamp))

def sendSyncRequestSuccess():
    rep.send(msgpack.packb(True))

#def removeExtraBytes(raw):
#    newBytes = raw
#    while newBytes[0] < 128:
#       newBytes = newBytes[1:]
#    return newBytes

#def addTimestampToStruct(data):
#    buffer = msgpack.unpackb(data)
#    buffer["timeStamp"] = round(time.time(), 3)
    # NOTE: timeStamp is a 64 bit Float or Double NOT a 32 bit float as is the case with the other data
#    return msgpack.packb(buffer)

def validCoordinate(coordinate):
    if len(coordinate) != 2:
       return False
    lat = coordinate[0]
    lon = coordinate[1]
    return (lat != 0.0) and (lat != -1.0) and (lon != 0.0) and (lon != -1.0)

def addSuppData(m):
    global previousBoatCoordinates
    global previousBoatTimestamp

    timestamp = round(time.time(), 3)
    m["timeStamp"] = timestamp

    boatC = gps.getCoordinates()
    # boatC = [10.0, 10.0]
    m["posLat"] = boatC[0]
    m["posLon"] = boatC[1]

    speed = 0.0

    if len(previousBoatCoordinates) > 0 and validCoordinate(boatC) and validCoordinate(previousBoatCoordinates):
       distanceDelta = alignmentcalc.distanceBetween(previousBoatCoordinates[0], previousBoatCoordinates[1], boatC[0], boatC[1])
       timeDelta = timestamp - previousBoatTimestamp
       speed = round(distanceDelta / timeDelta, 3)

    if not validCoordinate(previousBoatCoordinates) or validCoordinate(boatC):
       previousBoatCoordinates = boatC
       previousBoatTimestamp = timestamp

    m["speed"] = speed

#    print("DATA, ", m)

    return m

#def addSupplementaryData(motordata):
#    print("call supp data")
#    global previousBoatCoordinates
#    global previousBoatTimestamp

#    print("before timestamp")

    # TIMESTAMP
#    timestamp = round(time.time(), 3)
#    motordata["timeStamp"] = timestamp
    # NOTE: timeStamp is a 64 bit Float or Double NOT a 32 bit float as is the case with the other data

#    print("after timestamp")

    # COORDINATES
#    boatC = gps.getCoordinates() # lat lon
#    motordata["posLat"] = boatC[0] # lat
#    motordata["posLon"] = boatC[1] # lon
#    motordata["posLat"] = 1.0
#    motordata["posLon"] = 1.0

#    print("after pos")

    # SPEED
#    speed
#    if len(previousBoatCoordinates) > 0 and validCoordinate(boatC) and validCoordinate(previousBoatCoordinates):
#        distanceDelta = alignmentcalc.distanceBetween(previousBoatCoordinates[0], previousBoatCoordinates[1], boatC[0], boatC[1])
#        timeDelta = timestamp - previousBoatTimestamp
#        speed = round(distanceDelta / timeDelta, 3)

#    if not validCoordinate(previousBoatCoordinates) or validCoordinate(boatC):
#        previousBoatCoordinates = boatC
#        previousBoatTimestamp = timestamp


def enforceDataPackTypes(motordata):

    # ALL FLOATS ARE 64 BIT / EQUIVALENT TO DOUBLE

    motordata["TP"] = int(motordata["TP"])
    motordata["DP"] = int(motordata["DP"])
    motordata["CP"] = float(motordata["CP"] / 100.0)
    motordata["BV"] = float(motordata["BV"] / 100.0)
    motordata["UV"] = bool(motordata["UV"])
    motordata["SM"] = bool(motordata["SM"])
    motordata["EN"] = bool(motordata["EN"])
    motordata["BC"] = float(motordata["BC"] / 100.0)

    return motordata


def readFromArduino(queue, exit_event):
     while not exit_event.is_set():
         b = motorctrl.read()
#         print("read data from mtrctrl: ", b)

         try:
            motordata = msgpack.unpackb(b)
         except Exception:
            logging.critical("invalid mtrctrl data")
            continue

         motordata = enforceDataPackTypes(motordata)
#         motordata = addSupplementaryData(motordata)
#         print("before adding data to queue")
         queue.put(motordata)

         print(motordata)
         logging.info("Producer received data")
         time.sleep(0.01)


def broadcastDataZmq(queue, exit_event):
    '''Broadcast data with ZeroMQ.'''
    while not exit_event.is_set() or not queue.empty():
        try:
            # queue.get(True, 2) blocks with a 2 second timeout
            # If still empty after 2 seconds, throws Queue.Empty
            data = queue.get(True, 2)
 #           print("GOT DATA")
            #data = addSupplementary(data)
            data = addSuppData(data)
            logging.info(data)
            pub.send(msgpack.packb(data))
            logging.info('Consumer sending data. Queue size is %d.', queue.qsize())
        except Queue.Empty:
            pass    # no message ready yet
        except:
            traceback.print_exc()
            exit_event.set()
    logging.info('Consumer received event. Exiting now.')
    pub.close()

def receiveTimestampSync(exit_event):
    while not exit_event.is_set():
        try:
            newTimestamp = msgpack.unpackb(rep.recv(flags=zmq.NOBLOCK))
            logging.info("Updating timestamp with %d", newTimestamp)
            updateSystemTime(newTimestamp)
            sendSyncRequestSuccess()
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
#                logging.info("no timestamp update msg")
                pass    # no message ready yet
            else:
                traceback.print_exc()
        except:
            traceback.print_exc()
            exit_event.set()
        time.sleep(1)

def receiveMotorStatus(exit_event):
    while not exit_event.is_set():
        try:
            m = msgpack.unpackb(pair.recv(flags=zmq.NOBLOCK))
 #           logging.info("Received new motor status")
 #           print("sending mtr status: ", motorStatus)
            motorctrl.updateMotorStatus(m)
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
#                logging.info("no motor status update msg")
                motorctrl.sendMotorStatus()
                pass
            else:
                traceback.print_exc()
        except:
            traceback.print_exc()
            exit_event.set()
        time.sleep(1)

if __name__ == '__main__':
    try:
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=log_level, datefmt="%H:%M:%S")
        # Set up data queue
        pipeline = queue.Queue(maxsize=100)
        # Create exit event
        exit_event = threading.Event()
        # Spawn worker threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.submit(readFromArduino, pipeline, exit_event)
            executor.submit(broadcastDataZmq, pipeline, exit_event)
            executor.submit(receiveTimestampSync, exit_event)
            executor.submit(receiveMotorStatus, exit_event)
    except KeyboardInterrupt:
        logging.info('Setting exit event.')
        exit_event.set()
    except:
        traceback.print_exc()
        exit_event.set()
