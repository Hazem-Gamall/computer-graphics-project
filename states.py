from email.headerregistry import Group
from enum import Enum
from uiPanel import UiPanel
import pygame

class SubState(Enum):
    NEUTRAL = 1
    LINE = 2
    TRIANGLE = 3
    RECTANGLE = 4
    PENTAGON = 5
    CIRCLE = 6
    ELLIPSE = 7


class BaseState():
    def __init__(self, game) -> None:
        self.game = game
        self.sub_state:SubState = SubState.NEUTRAL
    def update(self):
        ...

    def draw(self):
        ...


class DrawState(BaseState):
    def __init__(self,game) -> None:
        super().__init__(game)
        self.group = pygame.sprite.Group()
    
    def update(self):
        ...
    
    def draw(self):
        ...

class TransformState(BaseState):
    ...

class ClipState(BaseState):
    ...