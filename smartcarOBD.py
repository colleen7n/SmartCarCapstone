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

                                                       
#fetches RPM, MPH, Fuel Level, Engine Coolant Temp, Engine Load, Run Time since Engine Start
def obd_data():
    serial_address = "/dev/ttyUSB0"
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200 #ELM327 Baud rate
    ser.timeout = 1
    
    #we need to test if it works without the next 3 lines of code
    #s = 'ATe0' #init OBD
    #ser.write(s + '\r')
    #time.sleep(.4)
    
    #fetch data
    ser.flushInput()
    s = '01 0C 0D 2F 05 04 1F' #requests data
    ser.write(s + '\r')
    time.sleep(.4) #gives device time to communicate with CAN bus
    raw_data = ser.read(1024)
    print("raw data: ")
    print(raw_data)
    #interpret data
    raw = re.sub(r'\W+','',raw_data) #eliminates spaces and non hex characters
    
    rpm = raw[8:12] #data is from 08 to 11, in python syntax that 8 to 12
    rpm = ((256*int(rpm[0:2], 16))+int(rpm[2:4], 16))/4
    
    mph = int(raw[14:16], 16)
    
    fuel_level = raw[19:21]
    fuel_level = (int(fuel_level[0:2], 16))
    fuel_level = (.392157)*fuel_level
    fuel_level = "%.2f" % fuel_level
    
    engine_coolant_temp = raw[23:25]
    engine_coolant_temp = ((int(engine_coolant_temp[0:2], 16))-40)*9/5+32
    
    engine_load = raw[27:29]
    engine_load = (int(engine_load[0:2], 16))/2.55
    engine_load = "%.2f" % engine_load
    
    run_time = raw[32:36]
    run_time = ((256*int(run_time[0:2], 16))+int(run_time[2:4], 16))
    
    return rpm, mph, fuel_level, engine_coolant_temp, engine_load, run_time



#-----------------------------------------------------------------------------------------

#display error codes
def error_codes(serial_address):
    #fetch data
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200
    ser.timeout = 1
    ser.flushInput()
    s = '03'
    ser.write(s + '\r')
    time.sleep(.4) #gives device time to communicate with CAN bus
    raw_data = ser.read(1024)
    print("raw data: ")
    print(raw_data)
    #interpret data
    hex_data = re.sub(r'\W+','',raw_data) #eliminates spaces and non hex characters
    raw = hex_data + "0000000000000000000000" #0's buffer for lexing

    error_code_1 = raw[2:6]
    error_code_2 = raw[6:10]   
    error_code_3 = raw[10:14]  
    return error_code_1, error_code_2, error_code_3#, error_code_4, error_code_5



def interpret_error_code(error_code):
    if error_code[0] == "0":
        error_code = "P0" + error_code[1:4]
    elif error_code[0] == "1":
        error_code = "P1" + error_code[1:4]
    elif error_code[0] == "2":
        error_code = "P2" + error_code[1:4]
    elif error_code[0] == "3":
        error_code = "P3" + error_code[1:4]
    elif error_code[0] == "4":
        error_code = "C0" + error_code[1:4]
    elif error_code[0] == "5":
        error_code = "C1" + error_code[1:4]
    elif error_code[0] == "6":
        error_code = "C2" + error_code[1:4]
    elif error_code[0] == "7":
        error_code = "C3" + error_code[1:4]
    elif error_code[0] == "8":
        error_code = "B0" + error_code[1:4]
    elif error_code[0] == "9":
        error_code = "B1" + error_code[1:4]
    elif error_code[0] == "A":
        error_code = "B2" + error_code[1:4]
    elif error_code[0] == "B":
        error_code = "B3" + error_code[1:4]
    elif error_code[0] == "C":
        error_code = "U0" + error_code[1:4]
    elif error_code[0] == "D":
        error_code = "U1" + error_code[1:4]
    elif error_code[0] == "E":
        error_code = "U2" + error_code[1:4]
    elif error_code[0] == "F":
        error_code = "U3" + error_code[1:4]
    return error_code

#MAIN

#error codes
error_code_1, error_code_2, error_code_3 = error_codes("/dev/ttyUSB0")
error_code_1 = interpret_error_code(error_code_1)
error_code_2 = interpret_error_code(error_code_2)
error_code_3 = interpret_error_code(error_code_3)
print("error messages")
print(error_code_1, error_code_2, error_code_3)

#OBD info
flag = 0
while flag < 100:
    rpm, mph, fuel_level, engine_coolant_temp, engine_load, run_time = obd_data()
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
