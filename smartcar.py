import serial
import time
import string
import io
import os
import re


#intialize serial port
ser = serial.Serial("/dev/ttyUSB0")
ser.baudrate = 115200
ser.timeout = 1
exitflag = False
time.sleep(1)
ser.flushInput()
s = 'ATe0'
ser.write(s + '\r')

while exitflag != True:

    #prompt user for AT command
    #s = raw_input('Enter command --> ')
        # ATZ: initializes device
        # AT SP 0: sets protocol to search for protocol
        # E0: Echo Off
        # E1: Echo On
        # H0: Headers off
        # H1: Headers on
        #
        # 01 00: PID 00 command - responds with a message
        # 01 0C: request engine rpm. The response will be 41 0C xx xx. Convert last 4 #s to decimal, divide by 4 to get rpm.
        # 09 02 5: request VIN. we know that there are 5 lines coming.
        # 01 01: request how many trouble codes are currently stored
        # 01 0D: Vehicle speed in km/h
        # 01 0F: Intake air temperature (formula A-40)
        # 01 45: Relative throttle position (formula: (100/255)*A
        # 01 46: Ambient air temperautre
        # 01 51: Fuel Type
        # 01 52: Ethanol fuel % (formula: (199/255)*A
        # 
    
    #get rpm
    if ser.inWaiting()>0: ser.flushInput()
    #ser.flushInput()
    s = '010c'
    ser.write(s + '\r')
    time.sleep(1)
    #convert response
    raw = ser.read(15)
    print (raw)
    msg1 = re.sub(r'\W+','',raw)
    print (msg1)
    msg= msg1[4:8]
    print (msg)
    rpm = ((256*int(msg[0:2], 16))+int(msg[2:4], 16))/4
    print 'above rpm'
    
    # get mph
    if ser.inWaiting()>0: ser.flushInput()
    #ser.flushInput()
    s1 = '010d'
    ser.write(s1 + '\r')
    time.sleep(1)
    #convert response
    raw1 = ser.read(15)
    print(raw1)
    msg2 = re.sub(r'\W+','',raw1)
    print(msg2)
    msg3= msg2[4:8]
    print(msg3)
    mph = int(msg3[0:2], 16)
    print 'above mph'

    # get fuel level 
    if ser.inWaiting()>0: ser.flushInput()
    #ser.flushInput()
    s2 = '012f'
    ser.write(s2 + '\r')
    time.sleep(1)
    #convert response
    raw1 = ser.read(15)
    print(raw1)
    msg2 = re.sub(r'\W+','',raw1)
    print(msg2)
    msg3= msg2[4:6]
    print(msg3)
    fl1 = (int(msg3[0:2], 16))
    print(fl1)
    fl = (.392157)*fl1
    print'above fuel level'
    
    # get intake air temp
    if ser.inWaiting()>0: ser.flushInput()
    #ser.flushInput()
    s3 = '0146'
    ser.write(s3 + '\r')
    time.sleep(1)
    #convert response
    raw1 = ser.read(15)
    print(raw1)
    msg2 = re.sub(r'\W+','',raw1)
    print(msg2)
    msg3= msg2[4:6]
    print(msg3)
    temp1 = (int(msg3[0:2], 16)-40)
    temp = (temp1*(1.8)) + 32

    #display message to output window
    print ("RPM: ",rpm)
    print ("MPH: ",mph)
    print ("FL: ", fl)
    print ("temp: ",temp)
    
#close serial    
ser.close
print ('Serial is closed')
