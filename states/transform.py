from enum import Enum
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from audio_manager import AudioManager

from button import CallbackButton
from drawing_manager import DrawingManager
from event_manager import EventManager
from shapes import Shape
from states.base import BaseState
from collision_manager import check_shape_point_collision
import transformation_utils



class TransformSubstate(Enum):
    NEUTRAL = 1
    SCALING = 2
    TRANSLATION = 3
    ROTATION = 4
    PIVOT_ROTATION = 5
    PIVOT_SCALING = 6
    INPUT_WINDOW = 7


class TransformState(BaseState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.substate = TransformSubstate.NEUTRAL
        self.temp_shape: Shape = None
        self.input_window = pygame_gui.elements.UIWindow(
            pygame.Rect(500, 235, 340, 200), game.ui_manager
        )
        self.input_window.hide()

        CallbackButton(  # L  T  W  H
            pygame.Rect(40, 50, 70, 70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#translate_button"),
            callback=lambda event: self.change_substate(TransformSubstate.TRANSLATION),
        )

        CallbackButton(
            pygame.Rect(40 + 70+50,50,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#scale_button"),
            callback=lambda event: self.change_substate(TransformSubstate.SCALING),
        )

        CallbackButton(
            pygame.Rect(40,50+70+60,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#rotate_button"),
            callback=lambda event: self.change_substate(TransformSubstate.ROTATION)
        )

        CallbackButton(
            pygame.Rect(40+70+50, 50+70+60 ,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#pivot_scale_button"),
            callback=lambda event: self.change_substate(TransformSubstate.PIVOT_SCALING)
        )

        CallbackButton(
            pygame.Rect(40,50+70*2+60*2,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#pivot_rotate_button"),
            callback=lambda event: self.change_substate(TransformSubstate.PIVOT_ROTATION)
        )

        EventManager().register_event(pygame.MOUSEBUTTONDOWN, self.on_click)

    def on_click(self, event):
        if not self.substate in [
            TransformSubstate.NEUTRAL,
            TransformSubstate.INPUT_WINDOW,
        ]:
            if DrawingManager().check_collision_with_surface(event.pos):
                for shape in DrawingManager().shapes:
                    if check_shape_point_collision(shape, event.pos):
                        self.temp_shape = shape
                        self.create_input_window(self.substate)

    def create_input_window(self, type: TransformSubstate):
        transformation_lookup = {
            TransformSubstate.TRANSLATION: (0,["tx", "ty"], transformation_utils.translate),
            TransformSubstate.SCALING: (1,["sx", "sy"], transformation_utils.scale),
            TransformSubstate.ROTATION: (0,["angle"], transformation_utils.rotate),
            TransformSubstate.PIVOT_SCALING: (
                0,["sx", "sy", "px", "py"],
                transformation_utils.pivot_scale,
            ),
            TransformSubstate.PIVOT_ROTATION: (
                0,["angle", "px", "py"],
                transformation_utils.pivot_rotate,
            ),
        }

        self.change_substate(TransformSubstate.INPUT_WINDOW)

        defualt_value, input_params, transformation = transformation_lookup[type]
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

                transformation(self.temp_shape, *input_params)
                self.input_window.get_container().kill()
                self.input_window.hide()
                self.change_substate(TransformSubstate.NEUTRAL)
                ...

            submit_button = CallbackButton(
                pygame.Rect(95, 130, 125, 30),
                "Submit",
                self.game.ui_manager,
                self.input_window,
                callback=submit_callback,
            )
            self.input_window.show()

    def on_exit(self):
        EventManager().pop_event(pygame.MOUSEBUTTONDOWN, self.on_click)
