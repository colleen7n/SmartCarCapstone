import serial
import time
import string
import io
import os


#intialize serial port
ser = serial.Serial("/dev/ttyUSB0")
ser.baudrate = 115200
ser.timeout = 1
s = 'response'

while s != 'exit':

    #prompt user for AT command
    s = raw_input('Enter command --> ')
    ser.flushInput()
    ser.write(s + '\r')
    time.sleep(1)

    #print response
    msg = ser.read(1024)
    print (msg)

#close serial    
ser.close
print ('Serial is closed')
