from enum import Enum
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from audioManager import AudioManager

from button import CallbackButton
from drawingManager import DrawingManager
from eventManager import EventManager
from shapes import Line, Rectangle, Shape, Triangle


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

        CallbackButton(#L  T  W  H
            pygame.Rect(40,50,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#line_button"),
            callback=lambda event: self.create_shape(Line),
        )


        CallbackButton(
            pygame.Rect(40 + 70+50,50,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#rectangle_button"),
            callback=lambda event: self.create_shape(Rectangle),
        )
        

        CallbackButton(
            pygame.Rect(40,50+70+60,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#triangle_button"),
            callback=lambda event: self.create_shape(Triangle),
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
                if self.temp_shape.set_input(event.pos):
                    DrawingManager().register_shape(self.temp_shape)
                    self.change_substate(Substate.NEUTRAL)

    def change_substate(self, new_substate: Substate):
        self.substate = new_substate

    def create_shape(self, shape_class):
        AudioManager().play_sound("button_click")
        self.change_substate(Substate.SHAPE)
        self.temp_shape = shape_class()


class TransformState(BaseState):
    ...


class ClipState(BaseState):
    ...
