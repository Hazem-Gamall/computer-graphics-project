import sys
from audio_manager import AudioManager
from drawing_manager import DrawingManager
from drawing_utils.bresenham import bresenham
from drawing_utils.dda import dda
from event_manager import EventManager
from logger.logger import Logger
from singleton import Singleton
import pygame
from state_machine import StateMachine
from states import DrawState, TransformState, ClipState
import pygame_gui
from pygame_gui.core import ObjectID
from button import CallbackButton
import line_drawer

# this file is too big
# TODO:
# create a panel manager.


class Game(metaclass=Singleton):
    SCREEN_SIZE = (1366, 768)

    def initialize(self, screen):
        self.ui_manager = pygame_gui.UIManager(self.SCREEN_SIZE, "assets/theme.json")
        self.main_panel = None
        self.state_panel = None
        self.play_surface = None
        self.init_panels()
        StateMachine().initialize(self)
        EventManager().initialize()
        StateMachine().change_state(DrawState(self))
        self.screen = screen
        DrawingManager().initialize(self.play_surface)
        AudioManager().initialize()
        AudioManager().register_sound("hitmarker", "assets/sound/hitmarker.mp3")
        AudioManager().register_sound("button_click", "assets/sound/button_click.mp3")
        Logger().initialize(self)

    def draw(self):
        DrawingManager().draw()
        self.screen.blit(self.play_surface, (270, 80))

    def update(self):
        for event in pygame.event.get():
            EventManager().push(event)
            self.ui_manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if isinstance(event.ui_element, CallbackButton):
                    event.ui_element.callback(event)
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                line_drawer.change_drawer(event.text)
                
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
            callback=lambda event: StateMachine(self).change_state(DrawState(self)),
        )
        CallbackButton(
            pygame.Rect(0, 0, 169, 35),
            manager=self.ui_manager,
            container=self.main_panel,
            object_id=ObjectID("#transform_button"),
            anchors={"center": "center"},
            callback=lambda event: StateMachine(self).change_state(
                TransformState(self)
            ),
        )
        CallbackButton(
            pygame.Rect(169, 0, 169, 35),
            manager=self.ui_manager,
            container=self.main_panel,
            object_id=ObjectID("#clip_button"),
            anchors={"center": "center"},
            callback=lambda event: StateMachine(self).change_state(ClipState(self)),
        )

        pygame_gui.elements.UIDropDownMenu(
            ["DDA", "Bresenham"],
            "Bresenham",
            (1200, 5, 100, 30),
            self.ui_manager,
            self.main_panel,
        )

    def init_state_panel(self):
        self.state_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 80, 270, 688),
            manager=self.ui_manager,
            object_id=ObjectID("#state_panel"),
        )

    def init_play_surface(self):
        self.play_surface = pygame.Surface((1166, 941))
        self.play_surface.fill("#A5C5E7")
        from main import screen

        screen.blit(self.play_surface, (270, 80))
