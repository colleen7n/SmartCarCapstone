#Nhim, Colleen
#Portland State University ECE Capstone
#March 9, 2017

#This program is a basic GUI using KIVY with python 2.7.13
#It is just one grid view and is fully working to display variables

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

Builder.load_file('SmartCarCapstone.kv')

class HomeScreen(PageLayout):
    your_time = StringProperty()
    a=NumericProperty()
    b=NumericProperty()
    c=NumericProperty()
    d=NumericProperty()
    e=NumericProperty()
 
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        Clock.schedule_interval(self.set_time, 0.1)


    def set_time(self,dt):
        self.your_time = time.strftime("%m/%d/%Y \n     %H:%M")
        self.a=100
        self.b=11
        self.c=2
        self.d=2222
        self.e=3
        
class SmartCarCapstone(App):
    def build(self):
        return HomeScreen()

if __name__ == '__main__':
    SmartCarCapstone().run()
