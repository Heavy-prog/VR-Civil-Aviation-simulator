from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from datetime import datetime

# Simulated user data for demonstration purposes
USER_DATA = {
    "admin": {"password": "admin", "last_sign_in": None},
}

class SignInScreen(Screen):
    pass

class AdminDashboardScreen(Screen):
    def change_password(self):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        old_password_input = TextInput(hint_text="Enter Old Password", password=True, multiline=False)
        new_password_input = TextInput(hint_text="Enter New Password", password=True, multiline=False)
        confirm_password_input = TextInput(hint_text="Confirm New Password", password=True, multiline=False)

        popup_layout.add_widget(old_password_input)
        popup_layout.add_widget(new_password_input)
        popup_layout.add_widget(confirm_password_input)

        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        save_button = Button(
            text="Save",
            on_release=lambda _: self.save_password(
                old_password_input.text, new_password_input.text, confirm_password_input.text
            )
        )
        cancel_button = Button(text="Cancel", on_release=lambda _: popup.dismiss())
        button_layout.add_widget(save_button)
        button_layout.add_widget(cancel_button)

        popup_layout.add_widget(button_layout)

        popup = Popup(title="Change Password", content=popup_layout, size_hint=(0.8, 0.6))
        popup.open()

    def save_password(self, old_password, new_password, confirm_password):
        if USER_DATA["admin"]["password"] != old_password:
            self.show_message("Old password is incorrect!")
            return
        if new_password != confirm_password:
            self.show_message("New passwords do not match!")
            return
        if len(new_password) < 6:
            self.show_message("Password must be at least 6 characters long!")
            return

        USER_DATA["admin"]["password"] = new_password
        self.show_message("Password changed successfully!")

    def add_user(self):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        username_input = TextInput(hint_text="Enter Username", multiline=False)
        user_id_input = TextInput(hint_text="Enter User ID", multiline=False)
        password_input = TextInput(hint_text="Enter Password", password=True, multiline=False)

        popup_layout.add_widget(username_input)
        popup_layout.add_widget(user_id_input)
        popup_layout.add_widget(password_input)

        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        save_button = Button(
            text="Add User",
            on_release=lambda _: self.save_user(
                username_input.text, user_id_input.text, password_input.text
            )
        )
        cancel_button = Button(text="Cancel", on_release=lambda _: popup.dismiss())
        button_layout.add_widget(save_button)
        button_layout.add_widget(cancel_button)

        popup_layout.add_widget(button_layout)

        popup = Popup(title="Add User", content=popup_layout, size_hint=(0.8, 0.6))
        popup.open()

    def save_user(self, username, user_id, password):
        if not username or not user_id or not password:
            self.show_message("All fields are required!")
            return
        if user_id in USER_DATA:
            self.show_message("User ID already exists!")
            return

        USER_DATA[user_id] = {"username": username, "password": password, "last_sign_in": None}
        self.show_message(f"User '{username}' added successfully!")

    def delete_user(self):
        popup_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        user_id_input = TextInput(hint_text="Enter User ID to Delete", multiline=False)

        popup_layout.add_widget(user_id_input)

        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        delete_button = Button(
            text="Delete",
            on_release=lambda _: self.perform_delete(user_id_input.text)
        )
        cancel_button = Button(text="Cancel", on_release=lambda _: popup.dismiss())
        button_layout.add_widget(delete_button)
        button_layout.add_widget(cancel_button)

        popup_layout.add_widget(button_layout)

        popup = Popup(title="Delete User", content=popup_layout, size_hint=(0.8, 0.4))
        popup.open()

    def perform_delete(self, user_id):
        if user_id not in USER_DATA:
            self.show_message("User ID not found!")
            return
        if user_id == "admin":
            self.show_message("Cannot delete admin!")
            return

        del USER_DATA[user_id]
        self.show_message("User deleted successfully!")

    def view_users(self):
        user_list_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        scroll_view = ScrollView(size_hint=(1, 0.8))

        for user_id, details in USER_DATA.items():
            username = details.get("username", "N/A")
            last_sign_in = details.get("last_sign_in", "Never")
            user_info = f"ID: {user_id}\nName: {username}\nLast Sign-In: {last_sign_in}"
            user_label = Label(text=user_info, size_hint_y=None, height=80, valign="middle", halign="left")
            user_list_layout.add_widget(user_label)

        scroll_view.add_widget(user_list_layout)

        popup_layout = BoxLayout(orientation="vertical", padding=10)
        popup_layout.add_widget(scroll_view)

        close_button = Button(text="Close", size_hint_y=None, height=40, on_release=lambda _: popup.dismiss())
        popup_layout.add_widget(close_button)

        popup = Popup(title="User List", content=popup_layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_message(self, message):
        popup = Popup(
            title="Message",
            content=Label(text=message),
            size_hint=(0.8, 0.4),
        )
        popup.open()

class MyApp(App):
    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(SignInScreen(name='signin'))
        sm.add_widget(AdminDashboardScreen(name='admin_dashboard'))
        return sm

    def sign_in(self, user_type, user_id, password):
        if user_type == "Admin" and user_id in USER_DATA and USER_DATA[user_id]["password"] == password:
            USER_DATA[user_id]["last_sign_in"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.show_message("Admin Sign In Successful!")
            self.root.current = 'admin_dashboard'
        else:
            self.show_message("Invalid credentials, please try again.")

    def show_message(self, message):
        popup = Popup(
            title="Message",
            content=Label(text=message),
            size_hint=(0.8, 0.4),
        )
        popup.open()

KV = '''
ScreenManager:
    SignInScreen:
    AdminDashboardScreen:

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
                width: 200
                height: 200

            Label:
                text: "Sign In"
                font_size: 45
                color: 1, 1, 1, 1  # White text
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
                            background_normal: ''  # Ensures the color is used instead of a default texture
                            background_color: 0.902, 0.0, 0.0, 1  # Light red (#e60000)
                            on_release:
                                app.sign_in("Admin", admin_id.text, admin_password.text)  # Call sign_in on app

<AdminDashboardScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1  # White background
            Rectangle:
                size: self.size
                pos: self.pos

        # Top Ribbon (same as Sign In)
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
                width: 200
                height: 200
            Label:
                text: "Admin Dashboard"
                font_size: 45
                color: 1, 1, 1, 1  # White text
                halign: 'center'
                valign: 'middle'

        # Main content for functional buttons
        BoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 10

            Button:
                text: "Change Password"
                size_hint_y: None
                height: 50
                background_normal: ''  # Ensures the color is used instead of a default texture
                background_color: 0.902, 0.0, 0.0, 1
                on_release: root.change_password()

            Button:
                text: "Add User"
                size_hint_y: None
                height: 50
                background_normal: ''  # Ensures the color is used instead of a default texture
                background_color: 0.902, 0.0, 0.0, 1
                on_release: root.add_user()

            Button:
                text: "Delete User"
                size_hint_y: None
                height: 50
                background_normal: ''  # Ensures the color is used instead of a default texture
                background_color: 0.902, 0.0, 0.0, 1
                on_release: root.delete_user()

            Button:
                text: "View Users"
                size_hint_y: None
                height: 50
                background_normal: ''  # Ensures the color is used instead of a default texture
                background_color: 0.902, 0.0, 0.0, 1
                on_release: root.view_users()
            Button:
                text: "Log Out"
                size_hint_y: None
                height: 50
                background_normal: ''  # Ensures the color is used instead of a default texture
                background_color: 0.902, 0.0, 0.0, 1  # Light red (#e60000)
                on_release: app.root.current = 'signin'  # Navigate back to sign-in screen 'signin'  # Navigate back to sign-in screen
'''

if __name__ == '__main__':
    MyApp().run()
