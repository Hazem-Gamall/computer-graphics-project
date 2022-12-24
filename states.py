from enum import Enum
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from audioManager import AudioManager

from button import CallbackButton
from drawingManager import DrawingManager
from eventManager import EventManager
from shapes import Line, Rectangle, Shape, Triangle

from collisionManager import check_rect_point_collision
import transformations

class BaseState:
    def __init__(self, game) -> None:
        self.game = game
        self.substate = None
        self.game.reset_state_panel()

    def update(self):
        ...

    def draw(self):
        ...

    def on_click(self, event):
        ...

    def change_substate(self, new_substate):
        self.substate = new_substate

    def on_exit(self):
        ...



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
        if self.substate == DrawSubstate.SHAPE:
            print(event.pos)
            
            if DrawingManager().check_collision_with_surface(event.pos):
                AudioManager().play_sound("hitmarker")
                if self.temp_shape.set_input(event.pos):
                    DrawingManager().register_shape(self.temp_shape)
                    self.change_substate(DrawSubstate.NEUTRAL)


    def create_shape(self, shape_class):
        AudioManager().play_sound("button_click")
        self.change_substate(DrawSubstate.SHAPE)
        self.temp_shape = shape_class()


    def on_exit(self):
        EventManager().pop_event(pygame.MOUSEBUTTONDOWN, self.on_click)


class TransformSubstate(Enum):
    NEUTRAL = 1
    SCALING = 2
    TRANSLATION = 3
    ROTATION = 4
    INPUT_WINDOW = 5

class TransformState(BaseState):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.temp_shape: Shape = None
        self.input_window = pygame_gui.elements.UIWindow(pygame.Rect(500,235,340,200),game.ui_manager)
        self.input_window.hide()
        
        CallbackButton(#L  T  W  H
            pygame.Rect(40,50,70,70),
            manager=game.ui_manager,
            container=game.state_panel,
            object_id=ObjectID("#translate_button"),
            callback=lambda event: self.change_substate(TransformSubstate.TRANSLATION),
        )


        # CallbackButton(
        #     pygame.Rect(40 + 70+50,50,70,70),
        #     manager=game.ui_manager,
        #     container=game.state_panel,
        #     object_id=ObjectID("#rectangle_button"),
        #     callback=lambda event: self.create_shape(Rectangle),
        # )
        

        # CallbackButton(
        #     pygame.Rect(40,50+70+60,70,70),
        #     manager=game.ui_manager,
        #     container=game.state_panel,
        #     object_id=ObjectID("#triangle_button"),
        #     callback=lambda event: self.create_shape(Triangle),
        # )

        EventManager().register_event(pygame.MOUSEBUTTONDOWN, self.on_click)

    def on_click(self, event):
        if self.substate not in  [TransformSubstate.NEUTRAL, TransformSubstate.INPUT_WINDOW]:
            if DrawingManager().check_collision_with_surface(event.pos):
                for shape in DrawingManager().shapes:
                    if check_rect_point_collision(shape.get_bounding_rect() ,event.pos):
                        self.temp_shape = shape
                        print("creating window")
                        self.create_input_window(self.substate)
                    
                
    def create_input_window(self, type: TransformSubstate):

        if(type == TransformSubstate.TRANSLATION):
            self.change_substate(TransformSubstate.INPUT_WINDOW)
            tx_label = pygame_gui.elements.UILabel(pygame.Rect(15,38,50,30),"Tx",self.game.ui_manager, self.input_window)
            tx_text_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect(65,42,80,30), self.game.ui_manager,self.input_window, initial_text="0")

            ty_label = pygame_gui.elements.UILabel(pygame.Rect(160,38,50,30),"Ty",self.game.ui_manager, self.input_window)
            ty_text_entry = pygame_gui.elements.UITextEntryLine(pygame.Rect(210,42,80,30), self.game.ui_manager,self.input_window, initial_text="0")

            def submit_callback(event):
                try:
                    tx = float(tx_text_entry.get_text())
                    ty = float(ty_text_entry.get_text())
                except ValueError:
                    print("casting error")
                    return

                transformations.translate(self.temp_shape, (tx, ty))
                self.input_window.get_container().kill()
                self.input_window.hide()
                self.change_substate(TransformSubstate.NEUTRAL)

            submit_button = CallbackButton(pygame.Rect(95,105,125,30), "Submit", self.game.ui_manager, self.input_window, callback=submit_callback)
            self.input_window.show()

    def on_exit(self):
        EventManager().pop_event(pygame.MOUSEBUTTONDOWN, self.on_click)
    

class ClipState(BaseState):
    ...
