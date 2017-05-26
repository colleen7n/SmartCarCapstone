# Smart Car Device Project
# Matthew Konyndyk, Jasjit Singh, Alex Mendez, Colleen Nhim
# Portland State University
# v0.0 created 02/25/2017
# Last update: v0.7 05/06/2017

# This script is used to interface a USB ELM327 OBDII with the Raspberry Pi


#MPG =VSS * 7.718/MAF

import serial
import time
import string
import io
import os
import re

def get_data():                                                       
    serial_address = "/dev/ttyUSB0"
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200 #ELM327 Baud rate
    ser.timeout = 1
    #fetch data
    ser.flushInput()
    s = 'ATMA' #requests data
    ser.write(s + '\r')
    time.sleep(.2) #gives device time to communicate with CAN bus
    raw_data = ser.readline(999)
    print("raw data: ")
    print(raw_data)
    #interpret data
    #raw = re.sub(r'\W+','',raw_data) #eliminates spaces and non hex characters
    #print(raw)

serial_address = "/dev/ttyUSB0"
ser = serial.Serial(serial_address)
ser.baudrate = 115200 #ELM327 Baud rate
ser.timeout = 1

s = 'ATe0' #init OBD
ser.write(s + '\r')
time.sleep(.5)

s = 'ATAL' # allow long messages
ser.write(s +'\r')
time.sleep(.5)

s = 'ATSPB' # set CAN to 125 kbaud
ser.write(s + '\r')
time.sleep(.5)

i = 0
while i < 100:
    get_data()
    i += 1


