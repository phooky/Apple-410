#!/usr/bin/python3
import serial

print("opening port")
s = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
print("opened")
s.write(b'PS4\x03')
print("Sent pen select\n")
print("recv {}\n".format(s.read(100)))
