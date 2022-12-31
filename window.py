from pygame_gui.elements import UIWindow

class HideButtonUIWindow(UIWindow):

    def on_close_window_button_pressed(self):
        self.hide()