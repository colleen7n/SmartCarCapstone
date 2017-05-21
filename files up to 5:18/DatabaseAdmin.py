import pyrebase
from random import randrange
import requests
# email is alex.mendezghs@gmail.com
# password is SmartCar90210
'''
Last updated April 29, 4:06 PM
'''


def generate_id(database):
    '''

    :param database:
    :return:
    '''
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    new_id = ""
    passed = 0
    while passed == 0:
        for i in range(6):
            new_id += alphabet[randrange(len(alphabet))]
        print(new_id)
        check = database.child("busi").child(new_id).get().val()
        if check is None:
            print("This is a new ID")
            passed = 1
        else:
            print("This ID is not new")
        # end if-else
    # end while
    return new_id


def get_tude(tudetype):
    d = 0
    while d == 0:
        tude = float(input("Please enter your new "+tudetype+":"))
        if (tude < 180.0) & (tude > -180.0):
            d = 1
        else:
            print("Sorry, invalid input. Try again.")
        # end if-else
    # end while
    return tude


def get_business():
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
        b = input("Please enter your business type:")
        if (int(b) > 0) & (int(b) < 9):
            d = 1
        else:
            print("Sorry, invalid input. Try again.")
        # end if-else
    # end while
    return b


def get_image():
    print("Please have an image URL ready for this step.")
    d = 0
    while d == 0:
        url = str(input("Please input the image URL here:"))
        img = requests.get(url)
        if img.status_code == 200:
            if (url[len(url)-4:] == ".jpg") | (url[len(url)-4:] == ".jpg"):
                print("Image accepted.")
                d = 1
            else:
                print("Sorry, image must be .jpg or .png. Please try again.")
            # end if-else
        else:
            print("Sorry, unable to access url. Please try again.")
        # end if-else
    # end while
    return url


def dl_image(store_name, image_url):
    img = requests.get(image_url)
    img_type = image_url[len(image_url) - 4:]
    if img.status_code == 200:
        img_final = store_name + img_type
        with open(img_final, 'wb') as handler:
            handler.write(img.content)
            handler.close()
        # end with-as
        return img_final
    else:
        print("Error downloading image. I recommend starting the process again.")
        return "ERROR.jpg"
    # end if-else


def add_location(database, person, storages, latitude, longitude, businesstype, imageurl):
    '''

    :param database:
    :param person:
    :param latitude:
    :param longitude:
    :param businesstype:
    :param imageurl:
    :return:
    '''
    new_store = generate_id(database)
    print("Your new location ID is", new_store)
    d1 = {new_store: latitude}
    d2 = {new_store: longitude}
    d3 = {new_store: businesstype}
    store_image = dl_image(new_store, imageurl)
    store_image_location = 'ads/'+store_image
    d4 = {new_store: store_image_location}
    database.child("lati").update(d1, person['idToken'])
    database.child("logi").update(d2, person['idToken'])
    database.child("busi").update(d3, person['idToken'])
    database.child("imag").update(d4, person['idToken'])
    storages.child(store_image_location).put(store_image, person["idToken"])
    print(new_store, "has been added to the database. Remember the location and ID!")


def option1(database, person, storages):
    '''

    :param database:
    :param person:
    :return:
    '''
    print("Great! Give me the following values and I can right on that:")
    lati = get_tude("latitude")
    logi = get_tude("longitude")
    busi = get_business()
    imag = get_image()
    add_location(database, person, storages, lati, logi, busi, imag)


def option2(database, person, storages):
    gone = 0
    print("Time to delete a location from the database.")
    print("Location ID is required for this step")
    while gone == 0:
        ded_ID = input("Please input the location you want to delete here:")
        if database.child("lati").child(ded_ID).get().val() is None:
            print("Sorry, this ID does not exist in our database. Try again.")
        else:
            print(ded_ID, "is now being deleted from the database. Stand by...")
            database.child("lati").child(ded_ID).remove(person["idToken"])
            database.child("logi").child(ded_ID).remove(person["idToken"])
            database.child("busi").child(ded_ID).remove(person["idToken"])
            image_name = database.child("imag").child(ded_ID).get().val()
            if image_name[len(image_name) - 4:] == ".jpg":
                storages.child(image_name).put("del.jpg", user["idToken"])
            elif image_name[len(image_name) - 4:] == ".png":
                storages.child(image_name).put("del.png", user["idToken"])
            database.child("imag").child(ded_ID).remove(person["idToken"])
            gone = 1
        # end if-else
    # end while
    print(ded_ID, "has been successfully removed from the database.")


def option3(database, person, storages):
    print("So you want to update your location. Have your location ID ready.")
    g = 0
    d = 0
    while d == 0:
        local_id = input("Enter your location ID here:")
        check = database.child("lati").child(local_id).get().val()
        if check is None:
            print("This ID does not exist. Please try again")
        else:
            d = 1
        # end if-else
    # end while
    while g == 0:
        print("Here are your update options:")
        print("Option 1: Update Latitude/Longitude")
        print("Option 2: Update business type")
        print("Option 3: Update image")
        print("Option 4: Finish updating")
        opt = int(input("Please input your option now"))
        if opt == 1:
            newLat = get_tude("Latitude")
            newLon = get_tude("Longitude")
            d1 = {local_id: newLat}
            d2 = {local_id: newLon}
            database.child("lati").update(d1, person['idToken'])
            database.child("logi").update(d2, person['idToken'])
            print("Latitude and Longitude have been updated")
        elif opt == 2:
            newBusi = get_business()
            d3 = {local_id: newBusi}
            database.child("busi").update(d3, person['idToken'])
            print("Business type has been updated")
        elif opt == 3:
            newImag = get_image()
            store_image = dl_image(local_id, newImag)
            store_image_location = 'ads/' + store_image
            d4 = {local_id: store_image_location}
            database.child("imag").update(d4, person['idToken'])
            storages.child(store_image_location).put(store_image, person["idToken"])
            print("Image has been updated")
        elif opt == 4:
            print(local_id, "is now updated.")
            g = 1
        else:
            print("Invalid input. Please try again.")
        # end if-elif-else
    # end while


config = {
        "apiKey": "AIzaSyBPakJA1_9GCjfgpws8AMSGD2E1pWRTfi8",
        "authDomain": "adsonrpiusinggps.firebaseapp.com",
        "databaseURL": "https://adsonrpiusinggps.firebaseio.com",
        "storageBucket": "adsonrpiusinggps.appspot.com"
}

firebase = pyrebase.initialize_app(config)  # initialize contact with the database
db = firebase.database()  # store database info
storage = firebase.storage()  # store database images/files
auth = firebase.auth()  # database user management
print("Welcome to the Smart Car Device Database Manager!")
# em = input("Please enter your email:")
# pw = input("Now enter your password:")
# user = auth.sign_in_with_email_and_password(em, pw)
user = auth.sign_in_with_email_and_password("alex.mendezghs@gmail.com", "SmartCar90210")
print("I can't confirm if you're signed in or not, so just pretend you are")
done = 0
while done == 0:
    print("What would you like to do now? (Enter a number)")
    print("1: Add new location")
    print("2: Delete old location")
    print("3: Update location")
    print("4: Quit")
    option = input("Your choice: ")
    if option == "1":
        option1(db, user, storage)
    elif option == "2":
        print("Option 2!")
        option2(db, user, storage)
    elif option == "3":
        print("Option 3!")
        option3(db, user, storage)
    elif option == "4":
        print("Thanks for using this program. We hope to see you again soon.")
        done = 1
    else:
        print("Invalid option. Please try again.")
    # end if-else
# end while
print("Alright we're done here")
