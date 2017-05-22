'''
Alex Mendez
Smart Car Device Capstone Project
Portland State University
March 11, 2017 to May 28, 2017

Requires Python 3.4 or later due to pyrebase library
Pyrebase library found at https://github.com/thisbejim/Pyrebase
Requires Pillow library for displaying images
Pillow library found at https://python-pillow.org/
LATITUDE FIRST, LONGITUDE SECOND. ALWAYS.
LATITUDE FIRST, LONGITUDE SECOND. ALWAYS.
LATITUDE FIRST, LONGITUDE SECOND. ALWAYS.
LATITUDE FIRST, LONGITUDE SECOND. ALWAYS.
THIS RULE IS CRITICAL. DO NOT FORGET IT.
'''

import pyrebase
from PIL import Image
from math import cos, radians, sqrt, sin, atan2
import time
import json


def champ_get(base_latitude, base_longitude, location_list, business_type):  # determine the closest location
    champ = "none"
    champDistance = 10.000  # distance from user to closest location, in miles
    champLatitude = 0.000
    champLongitude = 0.000

    for i in location_list:
        contenderLatitude = offlineLatitudes[i]
        contenderLongitude = offlineLongitudes[i]
        contenderDistance = distance_calc(base_latitude, base_longitude, contenderLatitude, contenderLongitude)
        if (contenderDistance < champDistance) & (offlineBusinesses[i] == business_type):
            champ = i
            champDistance = contenderDistance
            champLongitude = contenderLongitude
            champLatitude = contenderLatitude
    if champ == "none":
        print("No nearby businesses found. Try a different business type or try again later.")
    return champ, champDistance, champLatitude, champLongitude


def dict_get(anySet, anyPoint, anyRange):  # generate a dictionary from database sections
    d = {}
    for i in anySet.each():
        if (i.val() >= anyPoint - anyRange) & (i.val() <= anyPoint + anyRange):
            d[i.key()] = i.val()
    return d


def dict_image(dict_i):  # dict_get but specifically for images
    d = {}
    for i in dict_i.each():
        d[i.key()] = i.val()
    return d


def dict_to_json(dictionary, filename):  # convert dictionaries to json files
    with open(filename, 'w') as fp:
        fp.write(json.dumps(dictionary))
        fp.close()
    # print(filename, 'has been successfully written')


def distance_calc(latitude1, longitude1, latitude2, longitude2):    # calculate distance between two GPS points
    phi1 = radians(latitude1)
    phi2 = radians(latitude2)
    phiD = radians(latitude2 - latitude1)
    lamD = radians(longitude2 - longitude1)
    a = sin(phiD / 2) ** 2 + cos(phi1) * cos(phi2) * sin(lamD / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371000 * 0.000621371 * c


def get_business():  # ask the user for the business type they want to look for
    d = 0
    while d == 0:
        print("Now, I need the business type. Here are your options:")
        print("Type 1: Convenience")
        print("Type 2: Gas")
        print("Type 3: Parking")
        print("Type 4: Motel/Hotel")
        print("Type 5: Restaurant (no parking)")
        print("Type 6: Restaurant (with parking)")
        print("Type 7: ATM")
        print("Type 8: Other")
        b = int(input("Please enter your business type:"))
        if (b > 0) & (b < 9):
            d = 1
        else:
            print("Sorry, invalid input. Try again.")
        # end if-else
    # end while
    return b


def get_tude(tudetype):
    d = 0
    while d == 0:
        tude = float(input("Please enter your new " + tudetype + ":"))
        if (tude < 180.0) & (tude > -180.0):
            d = 1
        else:
            print("Sorry, invalid input. Try again.")
        # end if-else
    # end while
    return tude


def images_get(locationList, StorageSet):   # download images from the database
    d = {}
    for i in locationList:
        imageLocation = db.child("imag").child(i).get().val()
        d[i] = imageLocation
        imageName = imageLocation[4:]
        StorageSet.child(imageLocation).download(imageName)
    return d


def locations_get(latiSet, longiSet, latitude, longitude):  # generate a list of locations within 50 miles
    latirange = (5+45) / 69  # valid range, in latitude degrees. 1 degree = 69 miles
    longirange = (74+45) / 69 - abs(cos(radians(latitude)))  # valid range, in longitude degrees
    validLongitudes = set()  # set of longitudes near our location
    validLatitudes = set()  # set of latitudes near our location
    for k in latiSet.each():
        if (k.val() >= latitude - latirange) & (k.val() <= latitude + latirange):
            validLatitudes.add(k.key())
    for k in longiSet.each():
        if (k.val() >= longitude - longirange) & (k.val() <= longitude + longirange):
            validLongitudes.add(k.key())
    return validLongitudes & validLatitudes  # give us the locations that are actually near


def option1():  # update your GPS location
    la = get_tude("Latitude")
    lo = get_tude("Longitude")
    return la, lo


def option2(lat1, lon1, location_list):  # find the nearest location based on gps coordinates
    b = get_business()
    ch, chD, chLa, chLo = champ_get(lat1, lon1, location_list, b)
    if ch != "none":
        print("There is a location", chD, "miles away from you!")
        champImage = offlineImages[ch]
        champImageName = champImage[4:]
        Image.open(champImageName).show()




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
dbImages = db.child("imag").get()

# now let's pretend we got a valid gps value from the gps module
gpsLatitude = -122.6809599  # latitude is south-north
gpsLongitude = 45.5105602  # remember, longitude is east-west

# latitudeRange = 50/69
# longitudeRange = 119 / 69 - abs(cos(radians(gpsLatitude)))
latitudeRange = 360
longitudeRange = 360

# get a dictionary filled with longitudes, latitudes, and business types
offlineLatitudes = dict_get(dbLatitudes, gpsLatitude, latitudeRange)
dict_to_json(offlineLatitudes, 'latitudes.json')
offlineLongitudes = dict_get(dbLongitudes, gpsLongitude, longitudeRange)
dict_to_json(offlineLongitudes, 'longitudes.json')
offlineBusinesses = dict_get(dbBusinesses, 5, 4)
dict_to_json(offlineBusinesses, 'businesses.json')
offlineImages = dict_image(dbImages)
dict_to_json(offlineImages, 'images.json')
# the dictionaries were made in case the files need to be transferred from Python 3 to Python 2

# give us the locations that are actually near us
validLocations = locations_get(dbLatitudes, dbLongitudes, gpsLatitude, gpsLongitude)
offlineImages = images_get(validLocations, storage)

print("smart car device ready for offline use for any location within 50 miles.")
'''
end_time = time.process_time()
et = time.time()
print(end_time - start_time)
print(et-st)
'''

# now we make our command-line gui
done = 0
while done == 0:
    print("What would you like to do now?")
    print("Your current latitude is", gpsLatitude)
    print("Your current longitude is", gpsLongitude)
    print("Here are your options:")
    print("Option 1: Update gps coordinates")
    print("Option 2: Get the nearest desired business location")
    print("Option 3: Quit the program")
    opt = input("Please enter your choice now:")
    if opt == "1":
        print("Option 1 chosen.")
        option1()
    elif opt == "2":
        print("Option 2 chosen.")
    elif opt == "3":
        done = 1
    else:
        print("Invalid choice. Please try again.")
    # end if-else
# end while
print("Thank you for using the database. We hope to see you again soon.")

'''
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
'''
