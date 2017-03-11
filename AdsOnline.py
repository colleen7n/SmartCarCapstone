# requires Python 3.4 or later due to pyrebase library
# requires Pillow library from https://python-pillow.org/

import pyrebase
from PIL import Image

config = {
    "apiKey": "AIzaSyBPakJA1_9GCjfgpws8AMSGD2E1pWRTfi8",
    "authDomain": "adsonrpiusinggps.firebaseapp.com",
    "databaseURL": "https://adsonrpiusinggps.firebaseio.com",
    "storageBucket": "adsonrpiusinggps.appspot.com"
}

firebase = pyrebase.initialize_app(config)  # initialize contact with the database

db = firebase.database()  # store database info

dbLatitudes = db.child("lati").get()  # gather all latitudes values from database
# print(latitudes.val()) # print what we've got
print("And now, latitudes")
for i in dbLatitudes.each():
    print(i.key(), i.val())

dbLongitudes = db.child("logi").get()  # gather all longitude values from database
# print(longitudes.val()) # print what we got
print("And now, longitudes")
for j in dbLongitudes.each():
    print(j.key(), j.val())

# now let's pretend we got a valid gps value from the gps module
gpsLatitude = 85.5  # and latitude is south-north
gpsLongitude = 55.1  # remember, longitude is east-west
validLongitudes = set()  # set of longitudes near our location
validLatitudes = set()  # set of latitudes near our location

for i in dbLatitudes.each():
    if (i.val() >= gpsLatitude - 20) & (i.val() <= gpsLatitude + 20):
        print("you are in")
        validLatitudes.add(i.key())
    else:
        print("get out of here loser")

for i in dbLongitudes.each():
    if (i.val() >= gpsLongitude-20) & (i.val() <= gpsLongitude + 20):
        print("you are in")
        validLongitudes.add(i.key())
    else:
        print("get out of here loser")

print(validLatitudes)
print(validLongitudes)
validLocations = validLongitudes & validLatitudes  # give us the locations that are actually near us
print(validLocations)

validImages = set()

for i in validLocations:  # get the image locations, but not the images themselves
    validImages.add(db.child("imag").child(i).get().val())

print(validImages)

storage = firebase.storage()  # required for image access/downloading

images = set()  # file names for the images
for i in validImages:
    imageName = i[4:]
    images.add(imageName)
    storage.child(i).download(imageName)

Image.open('L2.jpg').show()  # display an image that was downloaded onto the pc
