from states.base import BaseState
from enum import Enum
import pygame
from pygame_gui.core import ObjectID
from audio_manager import AudioManager

from button import CallbackButton
from drawing_manager import DrawingManager
from event_manager import EventManager
from shapes import Line, Rectangle, Triangle

class DrawSubstate(Enum):
    NEUTRAL = 1
    SHAPE = 2
    CIRCLE = 3
    ELLIPSE = 4


class DrawState(BaseState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.temp_shape = None
        self.substate = DrawSubstate.NEUTRAL
        CallbackButton(  # L  T  W  H
            pygame.Rect(40, 50, 70, 70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#line_button"),
            callback=lambda event: self.create_shape(Line),
        )

        CallbackButton(
            pygame.Rect(40 + 70 + 50, 50, 70, 70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#rectangle_button"),
            callback=lambda event: self.create_shape(Rectangle),
        )

        CallbackButton(
            pygame.Rect(40, 50 + 70 + 60, 70, 70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#triangle_button"),
            callback=lambda event: self.create_shape(Triangle),
        )

        EventManager().register_event(pygame.MOUSEBUTTONDOWN, self.on_click)


    def draw(self):
        ...

    def on_click(self, event):
        if self.substate == DrawSubstate.SHAPE:
            print(event.pos)

            if DrawingManager().check_collision_with_surface(event.pos):
                AudioManager().play_sound("hitmarker")
                if self.temp_shape.set_input(event.pos):
                    DrawingManager().register_shapes(self.temp_shape)
                    self.change_substate(DrawSubstate.NEUTRAL)

    def create_shape(self, shape_class):
        AudioManager().play_sound("button_click")
        self.change_substate(DrawSubstate.SHAPE)
        self.temp_shape = shape_class()

    def on_exit(self):
        EventManager().pop_event(pygame.MOUSEBUTTONDOWN, self.on_click)
