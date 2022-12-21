import sys
from eventManager import EventManager
from singleton import Singleton
import pygame
from button import ImageButton
from uiCanvas import UiCanvas
from uiPanel import UiPanel
from stateMachine import StateMachine
import states
class Game(metaclass=Singleton):
    SCREEN_SIZE = (1366, 768)

    def __init__(self) -> None:
        StateMachine().change_state(states.DrawState)
        self.main_ui_panel = UiPanel(
            pygame.image.load("assets/mainUiSurface.png"),
            (0, 0),
            pygame.sprite.Group(
                ImageButton(
                    (430, 18),
                    pygame.image.load("assets/drawButtonBase.png"),
                    pygame.image.load("assets/drawButtonSecondary.png"),
                ),
                ImageButton(
                    (430 + 169, 18),
                    pygame.image.load("assets/transformButtonBase.png"),
                    pygame.image.load("assets/transformButtonSecondary.png"),
                ),
                ImageButton(
                    (430 + 169*2, 18),
                    pygame.image.load("assets/clipButtonBase.png"),
                    pygame.image.load("assets/clipButtonSecondary.png"),
                ),
            ),
        )

        self.state_ui_panel = UiPanel(
            pygame.image.load("assets/stateUiSurface.png"),
            (0, self.main_ui_panel.height),
        )
      
        self.background_panel = UiPanel(pygame.image.load("assets/background.png"), (self.state_ui_panel.width, self.main_ui_panel.height))

        self.ui_canvas = UiCanvas(self.main_ui_panel, self.state_ui_panel, self.background_panel)


    def draw(self, screen: pygame.Surface):
        self.ui_canvas.draw(screen)
        StateMachine().state.dra

    def update(self):
        for event in pygame.event.get():
            EventManager().push(event)
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
        self.ui_canvas.update()