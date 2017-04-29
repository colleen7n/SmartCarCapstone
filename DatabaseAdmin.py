import pyrebase
from random import randrange
from os import rename
# email is alex.mendezghs@gmail.com
# password is SmartCar90210
'''

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
        print(check)
        if check is None:
            print("This is a new ID")
            passed = 1
        else:
            print("This ID is not new")
        # end if-else
    # end while
    return new_id


def add_location(database, person, latitude, longitude, businesstype, imagetype):
    '''

    :param database:
    :param person:
    :param latitude:
    :param longitude:
    :param businesstype:
    :param imagetype:
    :return:
    '''
    new_store = generate_id(database)
    print("Your new store ID is", new_store)
    d1 = {new_store: latitude}
    d2 = {new_store: longitude}
    d3 = {new_store: businesstype}
    d4 = {new_store: 'ads/'+new_store+imagetype}
    database.child("lati").update(d1, person['idToken'])
    database.child("logi").update(d2, person['idToken'])
    database.child("busi").update(d3, person['idToken'])
    database.child("imag").update(d4, person['idToken'])
    print(new_store, "has been added to the database. Remember the location and ID!")


def option1(database, person):
    '''

    :param database:
    :param person:
    :return:
    '''
    print("Great! Give me the following values and I can right on that:")
    lati = float(input("First, give me the latitude: "))
    logi = float(input("Next, give me the longitude: "))
    print("Now, I need the business type. Here are your options:")
    print("Type 1: Convenience")
    print("Type 2: Gas")
    print("Type 3: Parking")
    print("Type 4: Motel/Hotel")
    print("Type 5: Restaurant (no parking)")
    print("Type 6: Restaurant (with parking)")
    print("Type 7: Other")

def option2(database, person):
    gone = 0



config = {
        "apiKey": "AIzaSyBPakJA1_9GCjfgpws8AMSGD2E1pWRTfi8",
        "authDomain": "adsonrpiusinggps.firebaseapp.com",
        "databaseURL": "https://adsonrpiusinggps.firebaseio.com",
        "storageBucket": "adsonrpiusinggps.appspot.com"
}

firebase = pyrebase.initialize_app(config)  # initialize contact with the database
db = firebase.database()  # store database info
auth = firebase.auth()  # database user management
print("Welcome to the Smart Car Device Database Manager!")
em = input("Please enter your email: ")
pw = input("Now enter your password: ")
user = auth.sign_in_with_email_and_password(em, pw)
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
        option1(db, user)
    elif option == "2":
        print("Option 2!")
        # option2(db, user)
    elif option == "3":
        print("Option 3!")
        # option3(db, user)
    elif option == "4":
        print("Thanks for using this program. We hope to see you again soon.")
        done = 1
    else:
        print("Invalid option. Please try again.")
    # end if-else
# end while
print("Alright we're done here")

