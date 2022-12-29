import pygame_gui
from states.base import BaseState
from enum import Enum
import pygame
from pygame_gui.core import ObjectID
from audio_manager import AudioManager

from button import CallbackButton
from drawing_manager import DrawingManager
from event_manager import EventManager
from shapes import Line, Rectangle, Triangle, Circle, Shape, Ellipse

class DrawSubstate(Enum):
    NEUTRAL = 1
    SHAPE = 2
    CIRCLE = 3
    ELLIPSE = 4
    INPUT_WINDOW = 5


class DrawState(BaseState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.temp_shape: Shape = None
        self.substate = DrawSubstate.NEUTRAL

        self.input_window = pygame_gui.elements.UIWindow(
            pygame.Rect(500, 235, 340, 200), game.ui_manager
        )
        self.input_window.hide()


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

        CallbackButton(
            pygame.Rect(40+70+50, 50+70+60 ,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#circle_button"),
            callback=lambda event: self.create_shape(Circle)
        )

        CallbackButton(
            pygame.Rect(40,50+70*2+60*2,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#ellipse_button"),
            callback=lambda event: self.create_shape(Ellipse)
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

        elif self.substate == DrawSubstate.CIRCLE:
            if DrawingManager().check_collision_with_surface(event.pos):
                AudioManager().play_sound("hitmarker")
                self.temp_shape.set_input(event.pos) #cirlce center
                self.create_input_window(DrawSubstate.CIRCLE)

        elif self.substate == DrawSubstate.ELLIPSE:
            if DrawingManager().check_collision_with_surface(event.pos):
                AudioManager().play_sound("hitmarker")
                self.temp_shape.set_input(event.pos) #ellipse center
                self.create_input_window(DrawSubstate.ELLIPSE)


    #stolen from the transform state, bad code design
    #TODO: encapsulate input window creation somewhere else
    def create_input_window(self, type: DrawSubstate):
        drawing_lookup = {
            DrawSubstate.CIRCLE: (0,["radius"]),
            DrawSubstate.ELLIPSE: (0,["Xr", "Yr"]),
        }
        self.change_substate(DrawSubstate.INPUT_WINDOW)

        defualt_value, input_params = drawing_lookup[type]

        #TODO: encapsulate this
        drawing_position = [15, 38]
        text_entry_elements = []
        for i, param in enumerate(input_params):
            if i != 0 and i % 2 == 0:
                drawing_position[1] += 40
                drawing_position[0] = 15

            pygame_gui.elements.UILabel(
                pygame.Rect((drawing_position[0] % 210, drawing_position[1]), (50, 30)),
                param,
                self.game.ui_manager,
                self.input_window,
            )
            drawing_position[0] += 50
            text_entry_elements.append(
                pygame_gui.elements.UITextEntryLine(
                    pygame.Rect(drawing_position, (80, 30)),
                    self.game.ui_manager,
                    self.input_window,
                    initial_text=str(defualt_value),
                )
            )
            drawing_position[0] += 80 + 15

            def submit_callback(event):
                try:

                    for i, param in enumerate(input_params):
                        input_params[i] = float(text_entry_elements[i].get_text())
                except ValueError:
                    print("casting error")
                    return
                for params in input_params:
                    self.temp_shape.set_input(params)
                    # print("param:", params, "xr",self.temp_shape.xradius, "yr", self.temp_shape.yradius)
                self.input_window.get_container().kill()
                self.input_window.hide()
                DrawingManager().register_shapes(self.temp_shape)
                print("registered", self.temp_shape)
                self.change_substate(DrawSubstate.NEUTRAL)
                ...

            submit_button = CallbackButton(
                pygame.Rect(95, 130, 125, 30),
                "Submit",
                self.game.ui_manager,
                self.input_window,
                callback=submit_callback,
            )
            self.input_window.show()


    def create_shape(self, shape_class):
        AudioManager().play_sound("button_click")
        if shape_class == Circle:
            self.change_substate(DrawSubstate.CIRCLE)
        elif shape_class == Ellipse:
            self.change_substate(DrawSubstate.ELLIPSE)
        else:
            self.change_substate(DrawSubstate.SHAPE)
        self.temp_shape = shape_class()

    def on_exit(self):
        EventManager().pop_event(pygame.MOUSEBUTTONDOWN, self.on_click)
