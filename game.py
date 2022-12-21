import sys
from drawingManager import DrawingManager
from eventManager import EventManager
from singleton import Singleton
import pygame
from stateMachine import StateMachine
import states
import pygame_gui
from pygame_gui.core import ObjectID
from button import CallbackButton

#this file is too big
#TODO:
    #create a panel manager.

class Game(metaclass=Singleton):
    SCREEN_SIZE = (1366, 768)


    def initialize(self, screen):
        self.ui_manager = pygame_gui.UIManager(self.SCREEN_SIZE, "assets/theme.json")
        self.main_panel = None
        self.state_panel = None
        self.play_surface = None
        self.init_panels()
        StateMachine().initialize(self)
        StateMachine().change_state(states.BaseState(self))
        self.screen = screen
        DrawingManager().initialize(self.play_surface)
        EventManager().initialize()

    def draw(self):
        DrawingManager().draw()
        self.screen.blit(self.play_surface, (270,80))

    def update(self):
        for event in pygame.event.get():
            EventManager().push(event)
            self.ui_manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                event.ui_element.callback(event)
        StateMachine(self).update()

    def reset_state_panel(self):
        self.state_panel.get_container().kill()

    def init_panels(self):
        self.init_main_panel()
        self.init_state_panel()
        self.init_play_surface()

    def init_main_panel(self):

        self.main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 1366, 80),
            manager=self.ui_manager,
            object_id=ObjectID("#main_panel"),
        )

        CallbackButton(
            pygame.Rect(-169, 0, 169, 35),
            manager=self.ui_manager,
            container=self.main_panel,
            object_id=ObjectID("#draw_button"),
            anchors={"center": "center"},
            callback=lambda event: StateMachine(self).change_state(
                states.DrawState(self)
            ),
        )
        CallbackButton(
            pygame.Rect(0, 0, 169, 35),
            manager=self.ui_manager,
            container=self.main_panel,
            object_id=ObjectID("#transform_button"),
            anchors={"center": "center"},
            callback=lambda event: StateMachine(self).change_state(
                states.TransformState(self)
            ),
        )
        CallbackButton(
            pygame.Rect(169, 0, 169, 35),
            manager=self.ui_manager,
            container=self.main_panel,
            object_id=ObjectID("#clip_button"),
            anchors={"center": "center"},
            callback=lambda event: StateMachine(self).change_state(
                states.ClipState(self)
            ),
        )

    def init_state_panel(self):
        self.state_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 80, 270, 688),
            manager=self.ui_manager,
            object_id=ObjectID("#state_panel"),
        )

    def init_play_surface(self):
        self.play_surface = pygame.Surface((1166,941))
        self.play_surface.fill("#A5C5E7")
        from main import screen
        screen.blit(self.play_surface, (270,80))
