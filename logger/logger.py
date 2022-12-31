

from time import time
from typing import Dict, List

from numpy import kaiser
import pygame_gui
from singleton import Singleton
from window import HideButtonUIWindow

class Logger(metaclass=Singleton):
    
    def initialize(self, game, data: Dict[str, List]={}) -> None:
        self.game = game
        self.data = data
        self.horizontal_margin = 10
        self.vertical_margin = 1
        self.log_window = HideButtonUIWindow((300,100,530,300),game.ui_manager, "", resizable=True)
        self.text_box = pygame_gui.elements.UITextBox("", (0,0,500,300),game.ui_manager, container=self.log_window)
        self.set_visiblity(0)
    

    def set_data(self,data):
        self.data = data
        self.text_box.set_text(self.get_output())
        self.set_visiblity(1)

    def get_output(self):
        #TODO:string concatination isn't very performant
        output = ""
        headers = self.data.keys()
        header_string = ""
        for header in headers:
            output += header.ljust(self.horizontal_margin)
        output += "\n"*self.vertical_margin
        output += header_string
        for row in zip(*list(self.data.values())):
            for element in row:
                output += str(round(element,2)).ljust(self.horizontal_margin) 
            output += "\n"*self.vertical_margin 

        return output
    
    def set_visiblity(self, visible:int):

        if visible:
            self.log_window.show()
            self.text_box.show()
            if self.text_box.scroll_bar: self.text_box.scroll_bar.show()
        else:
            self.log_window.hide()
            self.text_box.hide()
            if self.text_box.scroll_bar: self.text_box.scroll_bar.hide()
    def __str__(self) -> str:
        return str(self.data)

if __name__ == "__main__":
    data = {
        "x":[1000,2,3,4,5],
        "y":[6,7,8,9,10],
        "z":[6,7,8,9,10],
        "w":[6,7,8,9,10],
        "s":[6,7,8,9,10],
    }

    l = Logger(data)
    print(l)
    l.get_output()
    