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
from io import StringIO
import time
import serial
import json
import re
import requests

def distance_calc(latitude1, longitude1, latitude2, longitude2):
    '''
    calculate distance between two gps points in terms of miles
    :param latitude1:
    :param longitude1:
    :param latitude2:
    :param longitude2:
    :return:
    '''
    phi1 = radians(latitude1)
    phi2 = radians(latitude2)
    phiD = radians(latitude2 - latitude1)
    lamD = radians(longitude2 - longitude1)
    a = sin(phiD / 2) ** 2 + cos(phi1) * cos(phi2) * sin(lamD / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371000 * 0.000621371 * c


def locations_get(latiSet, longiSet, latitude, longitude):
    '''

    :param latiSet: The
    :param longiSet:
    :param latitude:
    :param longitude:
    :return:
    '''
    latirange = 5 / 69  # valid range, in latitude degrees. 1 degree = 69 miles
    longirange = 74 / 69 - abs(cos(radians(latitude)))  # valid range, in longitude degrees
    validLongitudes = set()  # set of longitudes near our location
    validLatitudes = set()  # set of latitudes near our location
    for key in latiSet:
        if (latiSet[key] >= latitude - latirange) & (latiSet[key] <= latitude + latirange):
            validLatitudes.add(key)
    for kay in longiSet:
        if (longiSet[kay] >= longitude - longirange) & (longiSet[kay] <= longitude + longirange):
            validLongitudes.add(kay)
    return validLongitudes & validLatitudes  # give us the locations that are actually near us

def start_pyrebase():
    config = {
        "apiKey": "AIzaSyBPakJA1_9GCjfgpws8AMSGD2E1pWRTfi8",
        "authDomain": "adsonrpiusinggps.firebaseapp.com",
        "databaseURL": "https://adsonrpiusinggps.firebaseio.com",
        "storageBucket": "adsonrpiusinggps.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)  # initialize contact with the database
    return firebase.storage()


def get_new_region(region, token):
    base = 'https://firebasestorage.googleapis.com/v0/b/adsonrpiusinggps.appspot.com/o/'
    url = base + region + '.json?alt=media&token=' + token
    j = requests.get(url)
    jstring = str(j.json())
    jfinal = jstring.replace("'", '"')
    with open(region + '.json', 'w') as F:
        F.write(jfinal)
    F.close()
    return json.loads(jfinal)


start_time = time.time()  # time the program
# connect to firebase using pyrebase
storage = start_pyrebase()

# download the json file containing the whole database
t ='a92e6c3a-e78e-497b-9779-6ae94125e1dd'
reg = 'mydata'
d = get_new_region(reg, t)
print("C2- %s seconds ---" % (time.time() - start_time))

gpsLatitude = -122.6809599  # latitude is south-north
gpsLongitude = 45.5105602  # remember, longitude is east-west

# give us the locations that are actually near us
validLocations = locations_get(d['lati'], d['logi'], gpsLatitude, gpsLongitude)

# time to find the closest location
champion = "none"
champDistance = 1.000  # distance from user to closest location, in latitude/longitude degrees
champLatitude = 0.000
champLongitude = 0.000

for i in validLocations:
    contenderLatitude = d['lati'][i]
    contenderLongitude = d['logi'][i]
    contenderDistance = sqrt((contenderLatitude-gpsLatitude)**2 + (contenderLongitude-gpsLongitude)**2)
    if contenderDistance < champDistance:
        champion = i
        champDistance = contenderDistance
        champLongitude = contenderLongitude
        champLatitude = contenderLatitude

# time to calculate distance between both points in miles
currentDistance = distance_calc(gpsLatitude, gpsLongitude, champLatitude, champLongitude)
champImage = d['imag'][champion]
champImageName = champImage[4:]
storage.child(champImage).download(champImageName)
print('You are currently', currentDistance, 'miles away from', champion)
print("C3- %s seconds ---" % (time.time() - start_time))
# Image.open(champImageName).show()  # display an image that was downloaded onto the pc
# print("CE- %s seconds ---" % (time.time() - start_time))
