from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

class SignInScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(SignInScreen(name='signin'))
        sm.add_widget(SignUpScreen(name='signup'))
        return sm

    def sign_in(self, user_type, user_id, password):
        if user_id and password:
            self.show_message(f"{user_type} Sign In Successful!")
        else:
            self.show_message("Please fill in all fields.")

    def sign_up(self, first_name, last_name, user_id, password, confirm_password, province, city, address):
        if not all([first_name, last_name, user_id, password, confirm_password]):
            self.show_message("Please fill in all required fields.")
        elif password != confirm_password:
            self.show_message("Passwords do not match.")
        else:
            self.show_message("Sign Up Successful!")

    def show_message(self, message):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(
            title="Message",
            content=Label(text=message),
            size_hint=(0.8, 0.4),
        )
        popup.open()

KV = '''
ScreenManager:
    SignInScreen:
    SignUpScreen:

<SignInScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1  # White background
            Rectangle:
                size: self.size
                pos: self.pos

        # Top Ribbon
        BoxLayout:
            size_hint_y: None
            height: 150

            spacing: 10
            padding: 10
            canvas.before:
                Color:
                    rgba: 0.902, 0.0, 0.0, 1  # Light red (#e60000)
                Rectangle:
                    size: self.size
                    pos: self.pos

            Image:
                source: 'logo.png'  # Path to your logo image
                size_hint_x: None
                width:200
                height: 200

            Label:
                text: "Sign In"
                font_size: 20
                color: 1, 1, 1, 1  # White text
                text_size: self.size
                halign: 'center'
                valign: 'middle'

        # Main content
        BoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 10

            TabbedPanel:
                do_default_tab: False

                TabbedPanelItem:
                    text: 'Admin'
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: 10
                        padding: 10

                        TextInput:
                            id: admin_id
                            hint_text: "Admin ID"
                            multiline: False

                        TextInput:
                            id: admin_password
                            hint_text: "Password"
                            password: True
                            multiline: False

                        Button:
                            text: "Sign In"
                            size_hint_y: None
                            height: 50  # Reduced height
                            background_normal: ''  # Ensures the color is used instead of a default texture
                            background_color: 0.902, 0.0, 0.0, 1  # Light red (#e60000)
                            on_release:
                                app.sign_in("Admin", admin_id.text, admin_password.text)

                TabbedPanelItem:
                    text: 'Pilot'
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: 10
                        padding: 10

                        TextInput:
                            id: pilot_id
                            hint_text: "Pilot ID"
                            multiline: False

                        TextInput:
                            id: pilot_password
                            hint_text: "Password"
                            password: True
                            multiline: False

                        Button:
                            text: "Sign In"
                            size_hint_y: None
                            height: 50  # Reduced height
                            background_normal: ''  # Ensures the color is used instead of a default texture
                            background_color: 0.902, 0.0, 0.0, 1  # Light red (#e60000)
                            on_release:
                                app.sign_in("Pilot", pilot_id.text, pilot_password.text)

            Button:
                text: "Go to Sign Up"
                size_hint_y: None
                height: 50
                background_normal: ''  # Ensures the color is used instead of a default texture
                background_color: 0.902, 0.0, 0.0, 1  # Light red (#e60000)

                on_release: app.root.current = 'signup'

<SignUpScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1  # White background
            Rectangle:
                size: self.size
                pos: self.pos

        # Top Ribbon
        BoxLayout:
            size_hint_y: None
            height: 60
            spacing: 10
            padding: 10
            canvas.before:
                Color:
                    rgba: 0.902, 0.0, 0.0, 1  # Light red (#e60000)
                Rectangle:
                    size: self.size
                    pos: self.pos

            Image:
                source: 'logo.png'  # Path to your logo image
                size_hint_x: None
                width: 50

            Label:
                text: "Sign Up"
                font_size: 20
                color: 1, 1, 1, 1  # White text
                text_size: self.size
                halign: 'center'
                valign: 'middle'

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: 20
                spacing: 10

                Label:
                    text: "First Name (Required)"
                TextInput:
                    id: first_name
                    hint_text: "First Name (Required)"
                    multiline: False
                    size_hint_y: None
                    height: 40

                Label:
                    text: "Last Name (Required)"
                TextInput:
                    id: last_name
                    hint_text: "Last Name (Required)"
                    multiline: False
                    size_hint_y: None
                    height: 40

                Label:
                    text: "ID (Required)"
                TextInput:
                    id: user_id
                    hint_text: "ID (Required)"
                    multiline: False
                    size_hint_y: None
                    height: 40

                Label:
                    text: "Password (Required)"
                TextInput:
                    id: password_signup
                    hint_text: "Password (Required)"
                    password: True
                    multiline: False
                    size_hint_y: None
                    height: 40

                Label:
                    text: "Confirm Password (Required)"
                TextInput:
                    id: confirm_password
                    hint_text: "Confirm Password (Required)"
                    password: True
                    multiline: False
                    size_hint_y: None
                    height: 40

                Label:
                    text: "Province"
                TextInput:
                    id: province
                    hint_text: "Province"
                    multiline: False
                    size_hint_y: None
                    height: 40

                Label:
                    text: "City"
                TextInput:
                    id: city
                    hint_text: "City"
                    multiline: False
                    size_hint_y: None
                    height: 40

                Label:
                    text: "Address"
                TextInput:
                    id: address
                    hint_text: "Address"
                    multiline: False
                    size_hint_y: None
                    height: 40

                Button:
                    text: "Sign Up"
                    size_hint_y: None
                    height: 50
                    background_normal: ''  # Ensures the color is used instead of a default texture
                    background_color: 0.902, 0.0, 0.0, 1  # Light red (#e60000)
                    on_release:
                        app.sign_up(
                        first_name.text,
                        last_name.text,
                        user_id.text,
                        password_signup.text,
                        confirm_password.text,
                        province.text,
                        city.text,
                        address.text
                        )

                Button:
                    text: "Go to Sign In"
                    size_hint_y: None
                    height: 50
                    background_normal: ''  # Ensures the color is used instead of a default texture
                    background_color: 0.902, 0.0, 0.0, 1  # Light red (#e60000)
                    on_release: app.root.current = 'signin'
'''

if __name__ == '__main__':
    MyApp().run()
