#Nhim, Colleen
#Portland State University ECE Capstone
#March 9, 2017

#This program is a basic GUI using KIVY with python 2.7.13

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Ellipse, Line

class HomeScreen(GridLayout):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
##        self.cols = 2
##        self.add_widget(Label(text='RPM: '))
##        self.RPM = TextInput(multiline=False) #this is where you would call from script
##        self.add_widget(self.RPM)
##        self.add_widget(Label(text='MPG: '))
##        self.MPG = TextInput(multiline=False) #call function
##        self.add_widget(self.MPG)
##
        self.cols = 2
        self.add_widget(Label(text='RPM: '))
        self.add_widget(Label(text='MPG: '))
        self.add_widget(Label(text='TEMP: '))
        self.add_widget(Label(text='TRIP: '))
        

class SmartCarCapstone(App):

    def build(self):
        return HomeScreen()


if __name__ == '__main__':
    SmartCarCapstone().run()
