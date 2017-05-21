#this script returns dummy data for the purpose of testing the GUI without being in the car



import time
import string
import random
import io
import os
import re



def obd_data():
    
    time.sleep(1) #the real smartcar.py script takes about a second to return data
    
    
    rpm = random.randrange(500, 5000) #number between 500 and 5000?
    
    mph = random.randrange(0, 120) #number between 0.0 and 120.0
    
    fuel_level = random.uniform(0, 100) #number between 0.0 and 100.0
    
    engine_coolant_temp = random.randrange(90, 150) #usually between 90 and 150 degress
    
    engine_load = random.uniform(0, 100) #number between 0.0 and 100.0
    
    run_time = random.randrange(1, 10000)
    m, s = divmod(run_time, 60)
    h, m = divmod(m, 60)
    run_time = "%d:%02d:%02d" % (h, m, s)
    
    return rpm, mph, fuel_level, engine_coolant_temp, engine_load, run_time


a,b,c,d,e,f = obd_data()

#print("rpm",a)
#print("mph",b)
#print("fuel level",c)
#print("engine coolant temp",d)
#print("engine load",e)
#print("time since engine start",f)
