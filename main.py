from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivy.lang import Builder

from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)

from kivy.uix.widget import Widget


kv = """
<Logo>:
    Image:
        source: 'Images/logo.png'
        width: root.width - 20
        height: dp(100)
        allow_stretch: True
        keep_ratio: False
        top: root.top - 10
        pos: 10, 0


<LoginScreen>:
    md_bg_color: self.theme_cls.backgroundColor
    MDAnchorLayout:
        Logo:
        MDGridLayout:
            cols: 1
            row_force_default: True
            row_default_height: 70
            size_hint: (None, 0.5)
            width: min(300, root.width)
            center_x: 0.5
            MDTextField:
                mode: "filled"
                id: username
                multiline: False
                padding: [2,2]
                on_text_validate: root.validate_login(self, username.text, password.text)
                MDTextFieldHintText:
                    text: "Username"
                    text_color_normal: "#1D497C"
                    text_color_focus: "#1D497C"
            MDTextField:
                mode: "filled"
                id: password
                password: True
                multiline: False
                padding: [2,2]
                on_text_validate: root.validate_login(self, username.text, password.text)
                MDTextFieldHintText:
                    text: "Password"
                    text_color_normal: "#1D497C"
                    text_color_focus: "#1D497C"

<MainScreen>:
    md_bg_color: self.theme_cls.backgroundColor
    Logo:
    MDButton:
        on_touch_down: app.choose_device()
        style: "elevated"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDButtonIcon:
            icon: "plus"

        MDButtonText:
            text: "Select Device"

"""

sm = ScreenManager()

class Logo(MDWidget):
    pass

class LoginScreen(MDScreen):
    def validate_login(instance, value, username, password):
        if len(username) < 20:
            print("valid login")
            sm.current = "main"
        else:
            print("Invalid Login")
            #popup = MDPopup(content=MDLabel(text='Invalid Login'), size_hint=(None, None), size=(200, 80),
            #              title = "", separator_height = 0)
            #popup.open()

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

root_widget = Builder.load_string(kv)

class SentinelApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.last_clicked_button = None
        self.current_device = None
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))

        sm.current = 'login'

        return sm
    def choose_device(self):
        self.dialog = MDDialog(
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Choose Device",
            ),
            # -----------------------Supporting text-----------------------
            # -----------------------Custom content------------------------
            MDDialogContentContainer(
                MDDivider(),
                MDListItem(
                    MDListItemSupportingText(
                        text="Sentinel 1",
                    ),
                    id="1",
                    theme_bg_color="Custom",
                    on_release=self.change_color
                ),
                MDListItem(
                    MDListItemSupportingText(
                        text="Sentinel 2",
                    ),
                    id="2",
                    theme_bg_color="Custom",
                    on_release=self.change_color
                ),
                MDDivider(),
                orientation="vertical",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=self.close_dialog
                ),
                MDButton(
                    MDButtonText(text="Confirm"),
                    style="text",
                    on_release=self.confirm_device
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        #if(self.current_device):
        #    self.ids.current_device.md_bg_color = [0.2, 0.6, 0.8, 1]
        #    print(self.current_device)
        self.dialog.open()

    
    def close_dialog(self, *args):
        self.dialog.dismiss()

    def confirm_device(self, *args):
        self.dialog.dismiss()
        self.current_device = self.last_clicked_button.id

    def change_color(self, instance):
        # Reset the style of the previous button
        if self.last_clicked_button:
            self.last_clicked_button.md_bg_color = [0, 0, 0, 0] # Reset to default background

        # Highlight the current button
        instance.md_bg_color = [0.2, 0.6, 0.8, 1] # Example highlight color

        # Update the last clicked button reference
        self.last_clicked_button = instance
    
if __name__ == '__main__':
    SentinelApp().run()