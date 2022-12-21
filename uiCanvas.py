
from typing import List
from uiPanel import UiPanel


class UiCanvas():
    def __init__(self, *panels) -> None:
        self.panels = panels

    def draw(self, screen):
        for panel in self.panels:
            panel.draw(screen)
    
    def update(self):
        for panel in self.panels:
            panel.update()
    
    def add(self, panel:UiPanel):
        self.panels.append(panel)