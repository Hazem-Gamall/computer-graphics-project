import pygame

from button import Button

class UiPanel():
    def __init__(self, background_image: pygame.Surface, position, group: pygame.sprite.Group = pygame.sprite.Group()) -> None:
        super().__init__()
        self.background_image = background_image
        print(self.background_image.get_width(), self.background_image.get_height())
        self.surface = pygame.Surface((self.background_image.get_width(), self.background_image.get_height()))
        self.rect = self.background_image.get_rect(topleft = position)
        self.surface.blit(self.background_image, (0,0))

        self.group = group

    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height


    def attach(self, group: pygame.sprite.Group):
        self.group.add(group)

    def draw(self, screen: pygame.Surface):
        self.group.draw(self.surface)
        screen.blit(self.surface, self.rect)

    def update(self):
        self.group.update()
    