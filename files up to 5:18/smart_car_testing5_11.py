#Nhim, Colleen
#Portland State University ECE Capstone
#March 9, 2017

#This program is a basic GUI using KIVY with python 2.7.13
#It is just one grid view and is fully working to display variables
#This version is now able to run on raspberry pi
#and now we are working on impementing the real variables to display

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

#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
from picamera import PiCamera
from time import sleep

#this is calling the kv file for the raspberry pi
#this file is needed for the rasp OS
Builder.load_file('SmartCarCapstone5_6.kv')

#this line is importing OBD variables from "smartcarOBD" python script
#import smartcarOBD

camera = PiCamera()
camera.rotation = 180

class HomeScreen(PageLayout):
    your_time = StringProperty()
    #this creates the variables for the data coming from OBD2
    a=NumericProperty()
    b=NumericProperty()
    c=NumericProperty()
    d=NumericProperty()
    e=NumericProperty()
    f=StringProperty()
 
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        Clock.schedule_interval(self.set_time, 0.1)
      
        btn = Button(text="on Preview")
        btn.bind(on_press=self.on_prev)

        btn1 = Button(text="off Preview")
        btn1.bind(on_press=self.off_prev)

        for but in [btn, btn1]:
            self.add_widget(but)


    def set_time(self,dt):
        self.your_time = time.strftime("%m/%d/%Y \n     %H:%M")
        #setting the self to the OBD variable
##        self.a=smartcarOBD.a
##        self.b=smartcarOBD.b
##        self.c=smartcarOBD.c
##        self.d=smartcarOBD.d
##        self.e=smartcarOBD.e
##        self.f=smartcarOBD.f


    def on_prev(self, obj):
                camera.start_preview(fullscreen=False, window=(0,0,800,480))
    def off_prev(self, obj):
                camera.stop_preview()
        
class SmartCarCapstone(App):
    def build(self):
        return HomeScreen()

if __name__ == '__main__':
    SmartCarCapstone().run()
