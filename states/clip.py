from enum import Enum
import sys
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from audio_manager import AudioManager

from button import CallbackButton
from drawing_manager import DrawingManager
from event_manager import EventManager
from shapes import Line, Rectangle, Shape, Triangle
from shapes.shape_collection import ShapeCollection
from states.base import BaseState
from collision_manager import check_shape_collision, check_shape_point_collision
from clip_utils import clip_shape


class ClipSubstate(Enum):
    NEUTRAL = 1
    CLIPPING_WINDOW_CREATION = (2,)
    CLIPPING = 3


class ClipState(BaseState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.substate = ClipSubstate.NEUTRAL
        self.clipping_window: Rectangle = Rectangle()
        EventManager().register_event(pygame.MOUSEBUTTONDOWN, self.on_click)

    def update(self):
        if self.substate == ClipSubstate.CLIPPING_WINDOW_CREATION:
            if self.clipping_window.top_left_vertex == pygame.mouse.get_pos():
                x,y = pygame.mouse.get_pos()
                new_position = x+1, y+1    
            else:
                new_position = pygame.mouse.get_pos()
            self.clipping_window.bottom_right_vertex = new_position
            self.clipping_window.compute_vertices()

    def on_click(self, event):
        if DrawingManager().check_collision_with_surface(event.pos):

            if self.substate == ClipSubstate.NEUTRAL:

                self.clipping_window.top_left_vertex = event.pos
                self.clipping_window.bottom_right_vertex = event.pos
                self.clipping_window.compute_vertices()
                self.change_substate(ClipSubstate.CLIPPING_WINDOW_CREATION)
                DrawingManager().register_shapes(self.clipping_window)

            elif self.substate == ClipSubstate.CLIPPING_WINDOW_CREATION:

                DrawingManager().pop_shape(self.clipping_window)
                self.clipping_window.get_bounding_rect()
                shapes_to_clip = [shape for shape in DrawingManager().shapes if check_shape_collision(shape, self.clipping_window)]
                for shape in shapes_to_clip:
                    post_clip_lines = clip_shape(shape, self.clipping_window)
                    DrawingManager().pop_shape(shape)
                    DrawingManager().register_shapes(post_clip_lines)

                self.change_substate(ClipSubstate.NEUTRAL)

        ...

    def on_exit(self):
        EventManager().pop_event(pygame.MOUSEBUTTONDOWN, self.on_click)
