import sys
from eventManager import EventManager
from singleton import Singleton
import pygame
from button import ImageButton


class Game(metaclass=Singleton):
    SCREEN_SIZE = (1366, 768)

    def __init__(self) -> None:
        self.main_ui_surface = pygame.image.load("assets/mainUiSurface.png")
        self.state_ui_surface = pygame.image.load("assets/stateUiSurface.png")
        self.background_surface = pygame.image.load("assets/background.png")

        self.main_buttons_group = pygame.sprite.Group(
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
                (430 + 169 + 169, 18),
                pygame.image.load("assets/clipButtonBase.png"),
                pygame.image.load("assets/clipButtonSecondary.png"),
            ),
        )

    def draw(self, screen: pygame.Surface):
        screen.blits(
            [
                [self.main_ui_surface, (0, 0)],
                [self.state_ui_surface, (0, self.main_ui_surface.get_height())],
                [
                    self.background_surface,
                    (
                        self.state_ui_surface.get_width(),
                        self.main_ui_surface.get_height(),
                    ),
                ],
            ]
        )
        self.main_buttons_group.draw(screen)

    def update(self):
        for event in pygame.event.get():
            EventManager().push(event)
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
        self.main_buttons_group.update()
