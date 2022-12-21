import pygame

from eventManager import EventManager

class Button(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.pos = pos
		

class ImageButton(Button):
	def __init__(self, pos, base_image, secondary_image): 
		super().__init__(pos)
		self.base_image = base_image
		self.secondary_image = secondary_image
		self.image = base_image
		self.rect = self.image.get_rect(topleft=self.pos)

		event_manager = EventManager()
		event_manager.register_event(pygame.MOUSEBUTTONDOWN, self.on_mouse_button_down)
		event_manager.register_event(pygame.MOUSEBUTTONUP, self.on_mouse_button_up)



	def update(self):
		...

	def on_mouse_button_down(self, event):
		if(self.checkForInput(event.pos)):
			self.image = self.secondary_image

	def on_mouse_button_up(self, event):
		if(self.checkForInput(event.pos)):
			self.image = self.base_image

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def checkHover(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.image = self.secondary_image
		else:
			self.image = self.base_image


class TextButton(Button):
	def __init__(self, pos, image, text_input, font, base_color, hovering_color):
		super().__init__(pos)
		self.image = image
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=self.pos)
		self.text_rect = self.text.get_rect(center=self.pos)

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)