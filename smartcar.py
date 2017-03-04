# Smart Car Device Project
# Matthew Konyndyk, Jasjit Singh, Alex Mendez, Colleen Nhim
# Portland State University
# v0.0 created 02/25/2017
# Last update: v0.2 03/04/2017

# This script connects a Raspberry Pi to a USB ELM327 OBDII device and automatically prints RPM, MPH, Fuel Level, & Intake Air Temperature data to the console.



import serial
import time
import string
import io
import os
import re


#initializes serial port connection
def serial_port_init(serial_address):
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200
    ser.timeout = 1
    exitflag = False
    time.sleep(1)
    ser.flushInput()
    s = 'ATe0'
    ser.write(s + '\r')


# returns an array of raw data
def get_raw_data():
    if ser.inWaiting()>0: ser.flushInput()
    s = '01 0C 0D 2F 46 4' #fetches RPM, MPH, Fuel Level, Intake Air Temperature. We know there are 4 lines coming.
    ser.write(s + '\r')
    time.sleep(.25) #gives device time to communicate with CAN bus
    raw[0] = ser.readline
    raw[1] = ser.read(1)
    raw[2] = ser.read(1)
    raw[3] = ser.read(1)
    return(raw)


# converts an array of raw data to an array of decoded data
def decode_raw_data(raw_data):
    rpm = re.sub(r'\W+','',raw_data) #searches for a word following a hyphen?
        rpm = rpm[4:8]
        rpm = ((256*int(msg[0:2], 16))+int(msg[2:4], 16))/4
    mph = re.sub(r'\W+','',raw_data)
        mph = mph[4:8]
        mph = int(msg3[0:2], 16)
    fuel_level = re.sub(r'\W+','',raw1)
        fuel_level = fuel_level[4:6]
        fuel_level = (int(msg3[0:2], 16))
        fuel_level = (.392157)*fuel_level
    intake_air_temp = re.sub(r'\W+','',raw1)
        intake_air_temp = intake_air_temp[4:6]
        intake_air_temp = (int(msg3[0:2], 16)-40)
        intake_air_temp = (temp1*(1.8)) + 32
    return [rpm, mph, fuel_level, intake_air_temp]


# displays values in the console.
def print_values_to_console(data_array):
    print ("RPM: ",data_array[1])
    print ("MPH: ",data_array[2])
    print ("Fuel Level: ", data_array[3])
    print ("Intake Air Temperature: ",data_array[4])



# Main body
serial_port_init("/dev/ttyUSB0") # sets up connection with the serial port
raw_data = get_raw_data() # fetches a list of raw data
decoded_data = decode_raw_data(raw_data) #converts raw data to integer values
print_values_to_console(decoded_data) # displays the CAN data in the console
ser.close #close serial
