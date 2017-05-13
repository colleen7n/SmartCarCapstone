#Nhim, Colleen
#Portland State University ECE Capstone
#May 13, 2017

#This program is a basic GUI using KIVY with python 2.7.13
#Working: Page Layouts, Camera functionality, touch capability
#Working on: Getting the obd data to interact and display on GUI

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Ellipse, Line
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
import time

#these imports are for the PICAMERA
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
from picamera import PiCamera
from time import sleep

#these imports are for the OBD DATA
import serial
import time
import string
import io
import os
import re

#this is calling the kv file for the raspberry pi
#this file is needed for the rasp OS
Builder.load_file('SmartCarCapstone5_13.kv')

#this line is importing OBD variables from "smartcarOBD" python script
#import smartcarOBD

#importing camera function
camera = PiCamera()
camera.rotation = 180



class HomeScreen(PageLayout):
                                                    
#fetches RPM, MPH, Fuel Level, Engine Coolant Temp, Engine Load, Run Time since Engine Start
    def obd_data():
        serial_address = "/dev/ttyUSB0"
        ser = serial.Serial(serial_address)
        ser.baudrate = 115200 #ELM327 Baud rate
        ser.timeout = 1
        
        s = 'ATe0' #init OBD
        ser.write(s + '\r')
        time.sleep(.3)
        
        #fetch data
        ser.flushInput()
        s = '01 0C 0D 2F 05 04 1F' #requests data
        ser.write(s + '\r')
        time.sleep(.3) #gives device time to communicate with CAN bus
        raw_data = ser.read(1024)
        #print("raw data: ")
        #print(raw_data)
        #interpret data
        raw = re.sub(r'\W+','',raw_data) #eliminates spaces and non hex characters
        
        rpm = raw[8:12] #data is from 08 to 11, in python syntax that 8 to 12
        rpm = ((256*int(rpm[0:2], 16))+int(rpm[2:4], 16))/4
        
        mph = int(raw[14:16], 16)
        
        fuel_level = raw[19:21]
        fuel_level = (int(fuel_level[0:2], 16))
        fuel_level = (.392157)*fuel_level
        fuel_level = "%.2f" % fuel_level
        
        engine_coolant_temp = raw[23:25]
        engine_coolant_temp = ((int(engine_coolant_temp[0:2], 16))-40)*9/5+32
        
        engine_load = raw[27:29]
        engine_load = (int(engine_load[0:2], 16))/2.55
        engine_load = "%.2f" % engine_load
        
        run_time = raw[32:36]
        #print(run_time)
        run_time = ((256*int(run_time[0:2], 16))+int(run_time[2:4], 16))
        
        return rpm, mph, fuel_level, engine_coolant_temp, engine_load, run_time



    your_time = StringProperty()

    #this creates the variables for the data coming from OBD2
    #rpm=NumericProperty()
    #mph=NumericProperty()
    #fuel_level=NumericProperty()
    #engine_coolant_temp=NumericProperty()
    #engine_load=NumericProperty()
    #run_time=StringProperty()
 
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        Clock.schedule_interval(self.set_time, 0.1)
        #fetched OBD data every second
        Clock.schedule_interval(self.rpm, 1)
        Clock.schedule_interval(self.mph, 1)
        Clock.schedule_interval(self.fuel_level, 1)
        Clock.schedule_interval(self.engine_coolant_temp, 1)
        Clock.schedule_interval(self.engine_load, 1)
        Clock.schedule_interval(self.run_time,1)

        #creates two buttons for on and off camera functionality
        btn = Button(text="on Preview")
        btn.bind(on_press=self.on_prev)

        btn1 = Button(text="off Preview")
        btn1.bind(on_press=self.off_prev)

        for but in [btn, btn1]:
            self.add_widget(but)


    def set_time(self,dt):
        self.your_time = time.strftime("%m/%d/%Y \n     %H:%M")
        #setting the self to the OBD variable
        self.rpm=obd_data.rpm
        self.mph=obd_data.mph
        self.fuel_level=obd_data.fuel_level
        self.engine_coolant_temp=obd_data.engine_coolant_temp
        self.engine_load=obd_data.engine_load
        self.run_time=obd_data.run_time

        #grabs 6 obd data from smartcarOBD python script
        #self.rpm, self.mph, self.fuel_level, self.engine_coolant_temp, self.engine_load, self.run_time = smartcarOBD.get_obd_data()


    #function for turning camera on and off
    def on_prev(self, obj):
                camera.start_preview(fullscreen=False, window=(0,100,640,480))
    def off_prev(self, obj):
                camera.stop_preview()



        
class SmartCarCapstone(App):
    def build(self):
        return HomeScreen()

if __name__ == '__main__':
    SmartCarCapstone().run()
