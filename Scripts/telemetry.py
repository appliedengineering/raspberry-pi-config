
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
motorctrl = motorcontrollerdriver.motorcontrollerdriver("/dev/ttyUSB0", 9600)
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

#

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

    #print(" --- BEFORE SUPP DATA")

    global previousBoatCoordinates
    global previousBoatTimestamp

    # TIMESTAMP
    timestamp = round(time.time(), 3)
    m["timeStamp"] = timestamp

    # COORDINATES
    boatC = gps.getCoordinates()
    # boatC = [10.0, 10.0]
    m["posLat"] = boatC[0]
    m["posLon"] = boatC[1]

    # SPEED
    speed = 0.0
    if len(previousBoatCoordinates) > 0 and validCoordinate(boatC) and validCoordinate(previousBoatCoordinates):
        distanceDelta = alignmentcalc.distanceBetween(previousBoatCoordinates[0], previousBoatCoordinates[1], boatC[0], boatC[1])
        timeDelta = timestamp - previousBoatTimestamp
        speed = round(distanceDelta / timeDelta, 3)

    if not validCoordinate(previousBoatCoordinates) or validCoordinate(boatC):
        previousBoatCoordinates = boatC
        previousBoatTimestamp = timestamp

    m["speed"] = speed

    #print(" --- AFTER SUPP DATA")

    return m


def enforceDataPackTypes(motordata):

    # ALL FLOATS ARE 64 BIT / EQUIVALENT TO DOUBLE

    #print(" --- BEFORE ENFORCE")

    motordata["TP"] = int(motordata["TP"])
    motordata["DP"] = int(motordata["DP"])
    #motordata["CP"] = float(motordata["CP"] / 100.0)
    motordata["BV"] = float(motordata["BV"] / 100.0)
    #motordata["UV"] = bool(motordata["UV"])
    motordata["SM"] = bool(motordata["SM"])
    motordata["EN"] = bool(motordata["EN"])
    motordata["BC"] = float(motordata["BC"] / 100.0)

    #print(" --- AFTER ENFORCE")

    return motordata


def readFromArduino(exit_event):
     #print("readFromArduino")
     while not exit_event.is_set():
         b = motorctrl.read()
         #print("read data from mtrctrl: ", b)

         try:
            motordata = msgpack.unpackb(b)
         except Exception:
            logging.critical("invalid mtrctrl data")
            continue

         motordata = enforceDataPackTypes(motordata)
         #print("IN BETWEEN")
         motordata = addSuppData(motordata)
         #print("before adding data to queue")
         #queue.put(motordata)
         pub.send(msgpack.packb(motordata))

         print(motordata)
         #logging.info("Producer received data")
         time.sleep(0.01)

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
        # Create exit event
        exit_event = threading.Event()
        # Spawn worker threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(readFromArduino, exit_event)
            executor.submit(receiveTimestampSync, exit_event)
            executor.submit(receiveMotorStatus, exit_event)
    except KeyboardInterrupt:
        logging.info('Setting exit event.')
        exit_event.set()
    except:
        traceback.print_exc()
        exit_event.set()
