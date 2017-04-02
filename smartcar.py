# Smart Car Device Project
# Matthew Konyndyk, Jasjit Singh, Alex Mendez, Colleen Nhim
# Portland State University
# v0.0 created 02/25/2017
# Last update: v0.4 04/01/2017

# This script is used to interface a USB ELM327 OBDII with the Raspberry Pi


#MPG =VSS * 7.718/MAF

import serial
import time
import string
import io
import os
import re

                                                       
#fetches RPM, MPH, Fuel Level, Engine Coolant Temp, Engine Load, Run Time since Engine Start
def obd_data_1(serial_address):
    #fetch data
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200
    ser.timeout = 1
    ser.flushInput()
    s = '01 0C 0D 2F 05 04 1F'
    ser.write(s + '\r')
    time.sleep(.4) #gives device time to communicate with CAN bus
    raw_data = ser.read(1024)
    #interpret data
    hex_data = re.sub(r'\W+','',raw_data) #eliminates spaces and non hex characters
    return hex_data


def interpret_data(raw):
    rpm = raw[8:12]
    rpm = ((256*int(rpm[0:2], 16))+int(rpm[2:4], 16))/4
    mph = int(raw[14:16], 16)
    fuel_level = raw[19:21]
    fuel_level = (int(fuel_level[0:2], 16))
    fuel_level = (.392157)*fuel_level
    engine_coolant_temp = 0
    engine_load = 0
    run_time = 0
    return rpm, mph, fuel_level, engine_coolant_temp, engine_load, run_time


# Main body
serial_address = "/dev/ttyUSB0"
ser = serial.Serial(serial_address)
ser.baudrate = 115200
ser.timeout = 1
s = 'ATe0'
ser.write(s + '\r') 
time.sleep(.4)
ser = serial.Serial(serial_address)
flag = 0

while flag < 100:
    hex = obd_data_1(serial_address)
    print("hex")
    print(hex)
    flag+=1
    

ser.close #close serial
