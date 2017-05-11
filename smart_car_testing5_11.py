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

#this is calling the kv file for the raspberry pi
#this file is needed for the rasp OS
Builder.load_file('SmartCarCapstone.kv')

#this line is importing OBD variables from "dummydataforGUI" python script
import dummydataforGUI

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


    def set_time(self,dt):
        self.your_time = time.strftime("%m/%d/%Y \n     %H:%M")
        #setting the self to the OBD variable
        self.a=dummydataforGUI.a
        self.b=dummydataforGUI.b
        self.c=dummydataforGUI.c
        self.d=dummydataforGUI.d
        self.e=dummydataforGUI.e
        self.f=dummydataforGUI.f

        
class SmartCarCapstone(App):
    def build(self):
        return HomeScreen()

if __name__ == '__main__':
    SmartCarCapstone().run()
