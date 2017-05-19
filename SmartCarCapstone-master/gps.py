#!/usr/bin/env python
#-*- coding: utf-8 -*-

import serial
import time
import string
import io
import os
import re


class serial_device:
    def __init__(self, serialport, speed):
        self.device = serial.Serial(port=serialport, baudrate=speed, timeout=1)
#gps.device
#Serial<id=0x3ad2320, open=True>(port='com3', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)

gps=serial_device('com3',9600)
count =0
def get_cor():
#while (count<2):
    #print gps.device
    gps.device.flushInput()
    #time.sleep(1)
    text = gps.device.read(500)
    text1= re.split('\r\n',text)
    match = [s for s in text1 if "$GPRMC" in s]
    match = re.split(',',match[0])
    lat = float(match[3][0:2])+(float(match[3][2:9]))/60
    lat = str(lat) + " " +match[4]
    ltt= float(match[5][0:3])+(float(match[5][3:]))/60
    ltt = str(ltt)+ " " + match[6]
    cor= lat+" " +ltt
    speed = float(match[7])*1.15078
    speed = str(speed)+ " " +"MPH"
    #print cor
    #print 'new'
    #count = count+1
#print "bye"
    return cor

