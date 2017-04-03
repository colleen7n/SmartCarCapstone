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
def obd_data(serial_address):
    #fetch data
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200
    ser.timeout = 1
    ser.flushInput()
    s = '01 0C 0D 2F 05 04 1F'
    ser.write(s + '\r')
    time.sleep(.4) #gives device time to communicate with CAN bus
    raw_data = ser.read(1024)
    print("raw data: ")
    print(raw_data)
    #interpret data
    hex_data = re.sub(r'\W+','',raw_data) #eliminates spaces and non hex characters
    return hex_data


def interpret_data(raw):
    
    rpm = raw[8:12] #data is from 08 to 11, in python syntax that 8 to 12
    rpm = ((256*int(rpm[0:2], 16))+int(rpm[2:4], 16))/4
    
    mph = int(raw[14:16], 16)
    
    fuel_level = raw[19:21]
    fuel_level = (int(fuel_level[0:2], 16))
    fuel_level = (.392157)*fuel_level
    
    engine_coolant_temp = raw[23:25]
    engine_coolant_temp = ((int(engine_coolant_temp[0:2], 16))-40)*9/5+32
    
    engine_load = raw[27:29]
    engine_load = (int(engine_load[0:2], 16))/2.55
    
    run_time = raw[32:36]
    run_time = ((256*int(run_time[0:2], 16))+int(run_time[2:4], 16))
    
    return rpm, mph, fuel_level, engine_coolant_temp, engine_load, run_time



#01 0C 0D 2F 05 04 1F
# raw data:
# 00F
# 0: 41 0C 0F BA 0D 00
# 1: 2F E4 05 50 04 40 1F
# 2: 00 D9 00 00 00 00 00

# hex
# 00F041   0C 0FBA   0D 00   1   2F E4   05 50   04 40   1F 2   00D9   0000000000
# 000000   00 0011   11 11   1   11 12   22 22   22 22   23 3   3333   3333444444
# 012345   67 8901   23 45   6   78 90   12 34   56 78   90 1   2345   67890


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
    hex = obd_data(serial_address)
    print("hex")
    print(hex)
    
    rpm, mph, fuel_level, engine_coolant_temp, engine_load, run_time = interpret_data(hex)
    print("data")
    print("rpm: ", rpm)
    print("mph: ", mph)
    print("fuel level: ", fuel_level)
    print("engine coolant temp: ", engine_coolant_temp)
    print("engine load: ", engine_load)
    m, s = divmod(run_time, 60)
    h, m = divmod(m, 60)
    print "%d:%02d:%02d" % (h, m, s)
    
    flag+=1
    

ser.close #close serial
