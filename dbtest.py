import pyrebase

config = {
        "apiKey": "AIzaSyBPakJA1_9GCjfgpws8AMSGD2E1pWRTfi8",
        "authDomain": "adsonrpiusinggps.firebaseapp.com",
        "databaseURL": "https://adsonrpiusinggps.firebaseio.com",
        "storageBucket": "adsonrpiusinggps.appspot.com"
}
firebase = pyrebase.initialize_app(config)  # initialize contact with the database
db = firebase.database()  # store database info

latitudes = db.child("adsonrpiusinggps").child("lati").order_by_child("value").start_at(34.0).end_at(99.0).get()
for i in latitudes.each():
        print(i.key(), i.val())
