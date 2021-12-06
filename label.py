import copy
import pygame
import style


class Label(pygame.sprite.Sprite):
	"""A pygame GUI label."""
	def __init__(self, position, text, theme=style.pyquiz_theme, style=style.Style()):
		super().__init__()

		self.style = copy.copy(theme.label)
		self.style.update(style)

		self.set_text(text)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = position

	def set_text_color(self, color):
		self.style.text_color = color

	def set_text(self, newtext):
		self.image = self.style.font.render(newtext, 1, self.style.text_color)

	def draw(self):
		self.screen.blit(self.image, (self.rect))


if __name__ == '__main__':
	screen = pygame.display.set_mode((600, 600))
	clock = pygame.time.Clock()

	labels = pygame.sprite.Group()
	labels.add(Label((100, 100), "Hello World",
		style=style.Style(font=pygame.font.SysFont("Arial", 20)))
	)
	second = Label((100, 200), "GiovanniPython",
		style=style.Style(font=pygame.font.SysFont("Arial", 40), text_color="yellow"))
	labels.add(second)

	loop = True
	while loop:
		screen.fill(0)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				loop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					loop = False
		labels.draw(screen)
		pygame.display.update()
		clock.tick(60)

	pygame.quit()
