# Smart Car Device Project
# Matthew Konyndyk, Jasjit Singh, Alex Mendez, Colleen Nhim
# Portland State University
# v0.0 created 02/25/2017
# Last update: v0.5 03/11/2017

# This script connects a Raspberry Pi to a USB ELM327 OBDII device and automatic                                import time




import serial
import time
import string
import io
import os
import re

#GPS Module
class serial_device:
    def __init__(self, serialport, speed):
        self.device = serial.Serial(port=serialport, baudrate=speed, timeout=1)

gps=serial_device('com3',9600)
count =0
while (count<2):
    #print gps.device
    gps.device.flushInput()
    time.sleep(1)
    text = gps.device.read(250)
    text1 = text[text.find('$GPRMC,')+20:text.find(',0.',text.find('$GPRMC,')+3)]
    print text1
    print 'new'
    count = count+1
print "bye"




def get_serial_address():
    if ser = serial.Serial("/dev/ttyUSB0"):
        return "/dev/ttyUSB0"
    elif ser = serial.Serial("/dev/ttyUSB1"):
        return "/dev/ttyUSB1"
    elif ser = serial.Serial("/dev/ttyUSB2"):
        return "/dev/ttyUSB2"
    elif ser = serial.Serial("/dev/ttyUSB3"):
        return "/dev/ttyUSB3"
    else:
        return 0


# returns a string of basic raw data
def screen_1_raw_data(serial_address):
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200
    ser.timeout = 1
    ser.flushInput()
    s = '01 0C 0D 2F 67 5E'
    #01 OC 0D 2F #fetches RPM, MPH, Fuel Level, Engine Coolant Temp, Engine Fuel Rate, Range.
    ser.write(s + '\r')
    time.sleep(1) #gives device time to communicate with CAN bus
    raw = ser.read(1024)
    return(raw)


# returns a string of extra raw data
def screen_2_raw_data(serial_address):
    ser = serial.Serial(serial_address)
    ser.baudrate = 115200
    ser.timeout = 1
    ser.flushInput()
    s = '01 04 10 11 62 0F 5C'
    #fetches RPM, MPH, Fuel Level, Intake Air Temperature.
    ser.write(s + '\r')
    time.sleep(1) #gives device time to communicate with CAN bus
    raw = ser.read(1024)
    return(raw)








#def separate_data(raw_data):
#rpm: 41 0C 0A 24 

#rpm, mph: 41 0C 0A F0 0D 00 

# mph, rpm: 41 0D 00 0C 0B 14 

# rpm, mph, fl: 008 0: 41 0C 0A BC 0D 00 1: 2F 78 00 00 00 00 00 

#all 4: 00A 0: 41 0C 0A C0 0D 00 1: 2F 78 46 50 00 00 00


# converts an array of raw data to an array of decoded data
def decode_raw_data(raw_data):
    raw = re.sub(r'\W+','',raw_data) #eliminates spaces and non hex characters
    print(raw)
    rpm = raw[8:12]
    rpm = ((256*int(rpm[0:2], 16))+int(rpm[2:4], 16))/4
    mph = int(raw[14:16], 16)
    fuel_level = raw[19:21]
    fuel_level = (int(fuel_level[0:2], 16))
    fuel_level = (.392157)*fuel_level
    #intake_air_temp = intake_air_temp[4:6]
    #intake_air_temp = (int(msg3[0:2], 16)-40)
    #intake_air_temp = (temp1*(1.8)) + 32
    return rpm, mph, fuel_level
    #0080410C 0EA9 0D 00 12F 7C 0000000000


# displays values in the console.
def print_values_to_console(rpm,mph,fl):
    print ("RPM: ",rpm)
    print ("MPH: ",mph)
    print ("Fuel Level: ", fl)
    #print ("Intake Air Temperature: ",data[3])



# Main body
serial_address = get_serial_address()
ser = serial.Serial(serial_address)
ser.baudrate = 115200
ser.timeout = 1
s = 'ATe0'
ser.write(s + '\r') 
time.sleep(1)
ser = serial.Serial(serial_address)
flag = 0

while flag == 0:
    screen_1_raw = screen_1_raw_data(serial_address) # fetches a list of raw data
    screen_2_raw = screen_2_raw_data(serial_address) # fetches extra raw data
    print(screen_1_raw)
    print(screen_2_raw)
    #rpm, mph, fl = decode_raw_data(basic_raw) #converts raw data to integer values
    #print_values_to_console(rpm,mph,fl) # displays the CAN data in the console

ser.close #close serial
