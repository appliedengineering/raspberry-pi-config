# Telemetry ZeroMQ UDP Publisher
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
# Define the socket using the Context.
radio = context.socket(zmq.RADIO)
radio.connect('udp://224.0.0.1:28650')

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

while True:
    radio.send(msgpack.packb(modifyData(testData)), group='telemetry')
    print(f"Timestamp - {round(time.time(), 3)}")
    time.sleep(0.1)

radio.close()
context.term()
