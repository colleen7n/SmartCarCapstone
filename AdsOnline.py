'''
Alex Mendez
Smart Car Device Capstone Project
Portland State University
March 11, 2017 to May 28, 2017

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
    '''

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

    :param latiSet:
    :param longiSet:
    :param latitude:
    :param longitude:
    :return:
    '''
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
    return validLongitudes & validLatitudes  # give us the locations that are actually near


def dict_get(anySet, anyPoint, anyRange):
    '''

    :param anySet:
    :param anyPoint:
    :param anyRange:
    :return:
    '''
    d = {}
    for i in anySet.each():
        if (i.val() >= anyPoint - anyRange) & (i.val() <= anyPoint + anyRange):
            d[i.key()] = i.val()
    return d


def images_get(locationList, StorageSet):
    '''

    :param locationList:
    :param StorageSet:
    :return:
    '''
    d = {}
    for i in locationList:
        imageLocation = db.child("imag").child(i).get().val()
        d[i] = imageLocation
        imageName = imageLocation[4:]
        StorageSet.child(imageLocation).download(imageName)
    return d


def champ_get(locationList, LatiDict, LongiDict, gpsLati, gpsLong):
    '''

    :param locationList:
    :param LongiDict:
    :param LatiDict:
    :return:
    '''
    champ = "none"
    champDistance = 1.000  # distance from user to closest location, in latitude/longitude degrees
    champLatitude = 0.000
    champLongitude = 0.000

    for i in locationList:
        contenderLatitude = LatiDict[i]
        contenderLongitude = LongiDict[i]
        contenderDistance = sqrt((contenderLatitude - gpsLati) ** 2 + (contenderLongitude - gpsLong) ** 2)
        if contenderDistance < champDistance:
            champ = i
            champDistance = contenderDistance
            champLongitude = contenderLongitude
            champLatitude = contenderLatitude
    return champ, champDistance, champLatitude, champLongitude

start_time = time.process_time()
st = time.time()
print("getting database information now...")
config = {
        "apiKey": "AIzaSyBPakJA1_9GCjfgpws8AMSGD2E1pWRTfi8",
        "authDomain": "adsonrpiusinggps.firebaseapp.com",
        "databaseURL": "https://adsonrpiusinggps.firebaseio.com",
        "storageBucket": "adsonrpiusinggps.appspot.com"
}
firebase = pyrebase.initialize_app(config)  # initialize contact with the database
db = firebase.database()  # store database info
storage = firebase.storage()  # required for image access/downloading
dbLatitudes = db.child("lati").get()
dbLongitudes = db.child("logi").get()
dbBusinesses = db.child("busi").get()


# now let's pretend we got a valid gps value from the gps module
gpsLatitude = -122.6809599  # latitude is south-north
gpsLongitude = 45.5105602  # remember, longitude is east-west

latitudeRange = 50/69
longitudeRange = 119 / 69 - abs(cos(radians(gpsLatitude)))

# get a dictionary filled with longitudes, latitudes, and business types
offlineLatitudes = dict_get(dbLatitudes, gpsLatitude, latitudeRange)
offlineLongitudes = dict_get(dbLongitudes, gpsLongitude, longitudeRange)
offlineBusinesses = dict_get(dbBusinesses, 4, 3)

# give us the locations that are actually near us
validLocations = locations_get(dbLatitudes, dbLongitudes, gpsLatitude, gpsLongitude)
offlineImages = images_get(validLocations, storage)
print("smart car device ready for offline use")
# time to find the closest location
champion, champDist, champLati, champLong = champ_get(validLocations, offlineLatitudes, offlineLongitudes, gpsLatitude, gpsLongitude)
print(champion, champDist, champLong, champLati)

# time to calculate distance between both points in miles
currentDistance = distance_calc(gpsLatitude, gpsLongitude, champLati, champLong)
end_time = time.process_time()
et = time.time()
print(end_time - start_time)
print(et-st)

champImage = offlineImages[champion]
champImageName = champImage[4:]
storage.child(champImage).download(champImageName)
Image.open(champImageName).show()  # display an image that was downloaded onto the pc
