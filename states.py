from enum import Enum
import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from button import CallbackButton

class SubState(Enum):
    NEUTRAL = 1
    LINE = 2
    TRIANGLE = 3
    RECTANGLE = 4
    PENTAGON = 5
    CIRCLE = 6
    ELLIPSE = 7


class BaseState:
    def __init__(self, game) -> None:
        self.game = game
        self.sub_state: SubState = SubState.NEUTRAL
        self.game.reset_state_panel()

    def update(self):
        ...

    def draw(self):
        ...


class DrawState(BaseState):
    def __init__(self, game) -> None:
        super().__init__(game)
        CallbackButton(pygame.Rect(0,0,100,100),"hey",game.ui_manager,game.state_panel)
        CallbackButton(pygame.Rect(150,150,100,100),"hola",game.ui_manager,game.state_panel)

    def update(self):
        print("draw state update")

    def draw(self):
        ...


class TransformState(BaseState):
    ...


class ClipState(BaseState):
    ...
