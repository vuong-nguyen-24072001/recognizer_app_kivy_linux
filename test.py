from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen,ScreenManager,FadeTransition,SwapTransition, FallOutTransition,RiseInTransition
import cv2

flag_face = False

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

class KivyCamera(Screen):
    count = 0
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.event = Clock.schedule_interval(self.check_flag_face, 0.01)

    def check_flag_face(self, *args):
        global flag_face
        if flag_face == True:
            flag_face = False
            print("a")
            self.capture = cv2.VideoCapture(0)
            self.event = Clock.schedule_interval(self.update, 0.03)
            self.manager.current = "cam"

    def event_button(self, *args):
        self.capture = cv2.VideoCapture(0)
        self.event = Clock.schedule_interval(self.update, 0.03)

    def update(self, dt):
        global face_cascade
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.1,4)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
                self.count += 1
            if self.count == 20:
                print("true")
                self.event.cancel()
                self.capture.release()
                self.manager.current = "login"
                self.count = 0
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.ids.img.texture = image_texture

class Login(Screen):
    flag_save = True
    #init? super?
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        Clock.schedule_interval(self.check_user, 0.01)  

    def check_user(self, *args):
        pass
    
    def event_sign_in_with_face(self, *args):
        global flag_face
        #self.ids.id_loading.opacity = 1
        flag_face = True    

class CamApp(MDApp):
    def build(self):
        self.sm = ScreenManager(transition= FallOutTransition())
        self.sm.add_widget(Login(name='login'))
        self.sm.add_widget(KivyCamera(name='cam'))
        return self.sm


if __name__ == '__main__':
    CamApp().run()