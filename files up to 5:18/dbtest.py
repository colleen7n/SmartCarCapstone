import pyrebase

config = {
        "apiKey": "AIzaSyBPakJA1_9GCjfgpws8AMSGD2E1pWRTfi8",
        "authDomain": "adsonrpiusinggps.firebaseapp.com",
        "databaseURL": "https://adsonrpiusinggps.firebaseio.com",
        "storageBucket": "adsonrpiusinggps.appspot.com"
}

firebase = pyrebase.initialize_app(config)  # initialize contact with the database
db = firebase.database()  # store database info1
auth = firebase.auth()  # manage database info
storage = firebase.storage()
user = auth.sign_in_with_email_and_password("alex.mendezghs@gmail.com", "SmartCar90210")

image_name = "L1.png"
print(image_name, "must die")
if image_name[len(image_name)-4:] == ".jpg":
        storage.child("ads/"+image_name).put("del.jpg", user["idToken"])
elif image_name[len(image_name)-4:] == ".png":
        storage.child("ads/" + image_name).put("del.png", user["idToken"])

'''
# another unsuccessful test XDDDDD
print("L1.png must die")
storage.child("ads/L1.png").remove(user["idToken"])
'''


'''
# successful test
print("Lal must die")
db.child("Herp").child("Lal").remove(user["idToken"])
print("Alright give it a moment")
if db.child("Herp").child("Lal").get().val() is None:
        print("GOTTEM")
else:
        print("try again lul")
'''


'''
# unsuccessful test XD
latitudes = db.child("adsonrpiusinggps").child("lati").order_by_child("value").start_at(34.0).end_at(99.0).get()
for i in latitudes.each():
        print(i.key(), i.val())
'''
