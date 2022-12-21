import sys
import pygame
from game import Game
pygame.init()

screen = pygame.display.set_mode(Game.SCREEN_SIZE)
game = Game()
clock = pygame.time.Clock()
# testButton = TextButton((500,70), pygame.image.load("assets/drawButton.png") , "hey", pygame.font.Font("assets/test/font.ttf", 40), "#ffffff", "#d7fcd4")
# testButton = ImageButton((500,70), pygame.image.load("assets/drawButtonBase.png"), pygame.image.load("assets/drawButtonSecondary.png"))
while True:
    time_delta = clock.tick(60)/1000.0
   
    PLAY_MOUSE_POS = pygame.mouse.get_pos()

    # testButton.checkHover(PLAY_MOUSE_POS)

    # testButton.update(screen)
    game.update()
    game.ui_manager.update(time_delta)
    game.ui_manager.draw_ui(screen)
    
    pygame.display.update()
