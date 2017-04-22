'''
Alex Mendez
Smart Car Device Capstone Project
Portland State University
March 11, 2017

requires Python 3.4 or later due to pyrebase library
Pyrebase library found at https://github.com/thisbejim/Pyrebase
requires Pillow library for image displaying
Pillow library found at https://python-pillow.org/
'''

import pyrebase
from PIL import Image
from math import cos, radians, sqrt, sin, atan2
import time
import serial
import json
import re


def distance_calc(latitude1, longitude1, latitude2, longitude2):
    phi1 = radians(latitude1)
    phi2 = radians(latitude2)
    phiD = radians(latitude2 - latitude1)
    lamD = radians(longitude2 - longitude1)
    a = sin(phiD / 2) ** 2 + cos(phi1) * cos(phi2) * sin(lamD / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371000 * 0.000621371 * c


def locations_get(latiSet, longiSet, latitude, longitude):
    latirange = 5 / 69  # valid range, in latitude degrees. 1 degree = 69 miles
    longirange = 74 / 69 - abs(cos(radians(latitude)))  # valid range, in longitude degrees
    validLongitudes = set()  # set of longitudes near our location
    validLatitudes = set()  # set of latitudes near our location
    for k in latiSet.each():
        if (k.val() >= latitude - latirange) & (k.val() <= latitude + latirange):
            validLatitudes.add(k.key())
    for k in longiSet.each():
        if (k.val() >= longitude - longirange) & (k.val() <= longitude + longirange):
            validLongitudes.add(k.key())
    return validLongitudes & validLatitudes  # give us the locations that are actually near us


config = {
    "apiKey": "AIzaSyBPakJA1_9GCjfgpws8AMSGD2E1pWRTfi8",
    "authDomain": "adsonrpiusinggps.firebaseapp.com",
    "databaseURL": "https://adsonrpiusinggps.firebaseio.com",
    "storageBucket": "adsonrpiusinggps.appspot.com"
}

firebase = pyrebase.initialize_app(config)  # initialize contact with the database
db = firebase.database()  # store database info
storage = firebase.storage()  # required for image access/downloading
dbLatitudes = db.child("lati").get()  # gather all latitudes values from database
dbLongitudes = db.child("logi").get()  # gather all longitude values from database

# now let's pretend we got a valid gps value from the gps module
# GPS Module
'''
class serial_device:
    def __init__(self, serialport, speed):
        self.device = serial.Serial(port=serialport, baudrate=speed, timeout=1)

gps = serial_device('com3', 9600)
count = 0
while count < 2:
    # print gps.device
    gps.device.flushInput()
    time.sleep(1)
    text = gps.device.read(250)
    text1 = text[text.find('$GPRMC,')+20:text.find(',0.', text.find('$GPRMC,')+3)]
    coordinateFinder = r"([\d\.)]+"
    print(text1)
    print('new')
    count += 1
print("bye")
'''
gpsLatitude = -122.6809599  # latitude is south-north
gpsLongitude = 45.5105602  # remember, longitude is east-west

# give us the locations that are actually near us
validLocations = locations_get(dbLatitudes, dbLongitudes, gpsLatitude, gpsLongitude)

# time to find the closest location
champion = "none"
champDistance = 1.000  # distance from user to closest location, in latitude/longitude degrees
champLatitude = 0.000
champLongitude = 0.000

for i in validLocations:
    contenderLatitude = db.child("lati").child(i).get().val()
    contenderLongitude = db.child("logi").child(i).get().val()
    contenderDistance = sqrt((contenderLatitude-gpsLatitude)**2 + (contenderLongitude-gpsLongitude)**2)
    if contenderDistance < champDistance:
        champion = i
        champDistance = contenderDistance
        champLongitude = contenderLongitude
        champLatitude = contenderLatitude
# print(champion, champDistance, champLatitude, champLongitude)

# time to calculate distance between both points in miles
currentDistance = distance_calc(gpsLatitude, gpsLongitude, champLatitude, champLongitude)

champImage = db.child("imag").child(champion).get().val()
champImageName = champImage[4:]
storage.child(champImage).download(champImageName)
Image.open(champImageName).show()  # display an image that was downloaded onto the pc
