#Nhim, Colleen
#Portland State University ECE Capstone
#March 11, 2017

#This program is a basic GUI using KIVY with python 2.7.13
#The main purpose of this program is to create a GUI
#The home page gives access to button selects
#The following two pages give readings from the OBDII calculations

from kivy.base import runTouchApp
from kivy.lang import Builder


kv = '''

PageLayout:
    GridLayout:
        canvas:
            Color:
                rgba: 54/255., 100/255., 139/255., 1
            Rectangle:
                pos: self.pos
                size: self.size
        orientation: 'vertical'
        cols: 2
        
        Label:
            text: 'Smart Car Capstone Home Screen'
            halign: 'right'
            valign: 'middle'    
        Label:
            text: 'Direction: '
            text_size: cm(6), cm(4)
            halign: 'right'
            valign: 'top'
        Button:
            text: 'GPS'
            on_press: print("run GPS")
            font_size: 30
            background_color: (240/255., 240/255., 240/255., 1)
        Button:
            text: 'Back Up Camera'
            on_press: print("run Camera")
            font_size: 30
            background_color: (240/255., 240/255., 240/255., 1)
            
        Widget
        Label:
            text: 'Swipe Right to calculate car diagnostics'
            valign: 'bottom'


            
    GridLayout:
        canvas:
            Color:
                rgba: 96/255., 96/255., 96/255., 1
            Rectangle:
                pos: self.pos
                size: self.size
        cols: 3
        
        Label:
            text: 'RPM: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'MPH: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'FUEL LEVEL: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'ENGINE FUEL RATE: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'RANGE: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'ENGINGE COOLANT TEMP: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'



    GridLayout:
        canvas:
            Color:
                rgba: 136/255., 136/255., 136/255., 1
            Rectangle:
                pos: self.pos
                size: self.size
        cols: 3
        
        Label:
            text: 'ENGINE LOAD: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'MASS AIRFLOW RATE: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'RELATIVE THROTTLE POSITION: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'PERCENT TORQUE: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'INTAKE AIR TEMP: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
        Label:
            text: 'ENGINE OIL TEMP: '
            text_size: cm(4), cm(6)
            halign: 'center'
            valign: 'top'
            
'''

if __name__ == '__main__':
    runTouchApp(Builder.load_string(kv))
    
