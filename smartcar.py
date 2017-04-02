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

                                                       
#fetches RPM, MPH, Fuel Level, Engine Coolant Temp, MAF, ???
def obd_data_1(serial_address):
    #fetch data
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200
    ser.timeout = 1
    ser.flushInput()
    s = '01 0C 0D 2F 05 50'
    ser.write(s + '\r')
    time.sleep(1) #gives device time to communicate with CAN bus
    raw_data = ser.read(1024)
    #interpret data
    hex_data = re.sub(r'\W+','',raw_data) #eliminates spaces and non hex characters
    return hex_data


#fetches Relative Throttle Position, Engine Load, Percent Torque, Engine Fuel Rate, Run Time since Engine Start, Ambient Air Temp,
def obd_data_2(serial_address):
    #fetch data
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200
    ser.timeout = 1
    ser.flushInput()
    s = '01 45 04 61 5E 1F 46'
    ser.write(s + '\r')
    time.sleep(1) #gives device time to communicate with CAN bus
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
    #intake_air_temp = intake_air_temp[4:6]
    #intake_air_temp = (int(msg3[0:2], 16)-40)
    #intake_air_temp = (temp1*(1.8)) + 32
    return param1, value1, param2, value2, param3, value3, param4, value4, param5, value5, param6, value6


# Main body
serial_address = "/dev/ttyUSB0"
ser = serial.Serial(serial_address)
ser.baudrate = 115200
ser.timeout = 1
s = 'ATe0'
ser.write(s + '\r') 
time.sleep(1)
ser = serial.Serial(serial_address)
flag = 0

while flag < 50:
    hex1 = obd_data_1(serial_address)
    hex2 = obd_data_2(serial_address)
    print("hex1")
    print(hex1)
    print("hex2")
    print(hex2)
    flag+=1
    

ser.close #close serial
