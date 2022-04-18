# raspberry-pi-config
Configuration instructions for raspberry-pi

# Access Point Setup Instructions
https://forums.raspberrypi.com/viewtopic.php?t=200944

# Network Spec

Raspberry Pi Network DHCP range = `192.168.1.2 - 192.168.1.255`

Raspberry Pi PtP ip = `192.168.3.1`


Atomic Pi Network DHCP range = `192.168.2.2 - 192.168.2.255`

Atomic Pi PtP ip = `192.168.3.2`

# Boat Data ZMQ Network Spec

Raspberry Pi Boat Data Publish Socket Port = `5556`

Raspberry Pi Boat Timestamp Reply Socket Port = `55561`

# Boat Data Pack Spec

`TP` = Throttle Percentage `uint64_t` or `int` 

`DP` = Duty Percentage `uint64_t` or `int`

`CP` = Chip Temperature `double`

`BV` = Battery Voltage `double`

`UV` = Under Voltage Protection `bool`

`OV` = Over Voltage Protection `bool`

`SM` = Solar Mode `bool`

`EM` = Motor Enabled `bool`

`timeStamp` = Data Timestamp `double`

`posLat` = Position Latitude `double`

`posLon` = Position Longitude `double`

`speed` = Speed of boat in m/s `double`

# Boat Motor Serial Communication Spec

Consistently send `1` to motor controller to keep motor on

# Alignment ZMQ Network Spec

Raspberry Pi GPS Alignment Publish Socket Port = `5551`


Atomic Pi GPS Alignment Publish Socket Port = `5552`
