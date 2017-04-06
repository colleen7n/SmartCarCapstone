#Testing

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import StringProperty
from kivy.clock import Clock
import time
from kivy.base import runTouchApp
from kivy.lang import Builder

class PageLayout(Widget):
    #pass
    your_time = StringProperty()
    def __init__(self,**kwargs):
        super(PageLayout,self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        Clock.schedule_interval(self.set_time, 0.1)    

    def set_time(self,dt):
        self.your_time = time.strftime("%m/%d/%Y %H:%M")

class capstone(App):
    def build(self):
        return PageLayout()

if __name__== "__main__":
    capstone().run()

