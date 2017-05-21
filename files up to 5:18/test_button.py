from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from functools import partial
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180

class DemoBox(BoxLayout):
        def __init__(self,**kwargs):
                super(DemoBox, self).__init__(**kwargs)
                self.orientation ="vertical"

                btn = Button(text="on Preview")
                btn.bind(on_press=self.on_prev)

                btn1 = Button(text="off Preview")
                btn1.bind(on_press=self.off_prev)

                for but in [btn, btn1]:
                        self.add_widget(but)
        
        def on_prev(self, obj):
                camera.start_preview(fullscreen=False, window=(0,100,640,480))
        def off_prev(self, obj):
                camera.stop_preview()

class DemoApp(App):
        def build(self):
                return DemoBox()
if __name__== "__main__":
        DemoApp().run()

                

