from kivy.app import App

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
import json
import requests

Builder.load_string("""
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        GridLayout:
            rows: 3
            cols: 1
            padding: 10
            spacing: 10
            row_default_height: 30
            MDTextField:
                hint_text: "Email"
                id: usernamevalue
            MDTextField:
                hint_text: "Password"
                id: passwordvalue
                password: True
            MDRectangleFlatButton:
                text: 'Login'
                on_press: root.login_button_action()
<FailedLoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        MDLabel:
            text: "Login Failed"
        MDRectangleFlatButton:
            text: 'Back To Login'
            on_press: root.manager.current = 'login'
<TaskScreen>:
    ScrollView:
        MDList:
            id: tasklist
    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: app.theme_cls.primary_color
        x: root.width - self.width - dp(10)
        y: dp(10)
        on_press: root.manager.current = 'addtask'
""")

class FailedLoginScreen(Screen):
    pass


class TaskScreen(Screen):
    def on_enter(self):
        for i in range(10):
            self.ids.tasklist.add_widget(
                OneLineListItem(text=f"Filler task {i}")
            )


class LoginScreen(Screen):
    def build(self):
        pass
 
    def login_button_action(self):
        url = 'https://reqres.in/api/login'
        
        #data = json.dumps({"email": "eve.holt@reqres.in","password": "cityslicka"})
        data = json.dumps({"email": self.ids.usernamevalue.text,"password": self.ids.passwordvalue.text})

        response = requests.post(url, data=data, headers={'Content-Type':'application/json'})

        userdata = json.loads(response.text)

        if userdata.get("token"):
            self.manager.current = 'tasklist'
        else:
            self.manager.current = 'failedlogin'


class MainApp(MDApp):

    def build(self):
        sm = ScreenManager();
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(FailedLoginScreen(name='failedlogin'))
        sm.add_widget(TaskScreen(name='tasklist'))

        return sm

if __name__ == '__main__':
    MainApp().run()
