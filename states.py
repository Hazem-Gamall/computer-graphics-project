from enum import Enum
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from audioManager import AudioManager

from button import CallbackButton
from drawingManager import DrawingManager
from eventManager import EventManager
from shape import Shape


class Substate(Enum):
    NEUTRAL = 1
    SHAPE = 2
    CIRCLE = 3
    ELLIPSE = 4


class BaseState:
    def __init__(self, game) -> None:
        self.game = game
        self.substate: Substate = Substate.NEUTRAL
        self.game.reset_state_panel()

    def update(self):
        ...

    def draw(self):
        ...

    def on_click(self):
        ...

    def change_substate(self, new_substate: Substate):
        ...


class DrawState(BaseState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.temp_shape = None
        CallbackButton(
            pygame.Rect(40, 50, 70, 70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#line_button"),
            callback=lambda event: self.create_shape(2),
        )
        CallbackButton(
            pygame.Rect(150, 150, 100, 100), "hola", game.ui_manager, game.state_panel
        )
        EventManager().register_event(pygame.MOUSEBUTTONDOWN, self.on_click)

    def update(self):
        # print("draw state update")
        ...

    def draw(self):
        ...

    def on_click(self, event):
        if self.substate == Substate.SHAPE:
            print(event.pos)
            
            if DrawingManager().check_collision_with_surface(event.pos):
                AudioManager().play_sound("hitmarker")
                if self.temp_shape.set_vertex(event.pos):
                    DrawingManager().register_shape(self.temp_shape)
                    self.change_substate(Substate.NEUTRAL)

    def change_substate(self, new_substate: Substate):
        self.substate = new_substate

    def create_shape(self, num_of_vertices):
        self.change_substate(Substate.SHAPE)
        self.temp_shape = Shape(num_of_vertices)


class TransformState(BaseState):
    ...


class ClipState(BaseState):
    ...
