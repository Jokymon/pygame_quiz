
import pygame


pygame.init()
def fontsize(size):
	font = pygame.font.SysFont("Arial", size)
	return font


font_default = fontsize(20)


labels = pygame.sprite.Group()
class Label(pygame.sprite.Sprite):
	''' CLASS FOR TEXT LABELS ON THE WIN SCREEN SURFACE '''
	def __init__(self, screen, text, x, y, size=20, color="white"):
		super().__init__()

		if size != 20:
			self.font = fontsize(size)
		else:
			self.font = font_default
		self.image = self.font.render(text, 1, color)
		_, _, w, h = self.image.get_rect()
		self.rect = pygame.Rect(x, y, w, h)
		self.screen = screen
		self.text = text
		labels.add(self)

	def change_text(self, newtext, color="white"):
		self.image = self.font.render(newtext, 1, color)

	def change_font(self, font, size, color="white"):
		self.font = pygame.font.SysFont(font, size)
		self.change_text(self.text, color)

	def draw(self):
		self.screen.blit(self.image, (self.rect))


def show_labels():
	for label in labels:
		label.draw()


if __name__ == '__main__':
	# TEXT TO SHOW ON THE SCREEN AT POS 100 100
	win = pygame.display.set_mode((600, 600))
	clock = pygame.time.Clock()

	Label(win, "Hello World", 100, 100, 36)
	second = Label(win, "GiovanniPython", 100, 200, 24, color="yellow")
	second.change_font("Arial", 40, "yellow")
	# LOOP TO MAKE THINGS ON THE SCRREEN
	loop = True
	while loop:
		win.fill(0) # CLEAN THE SCREEN EVERY FRAME
		# CODE TO CLOSE THE WINDOW
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				loop = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					loop = False
		# CODE TO SHOW TEXT EVERY FRAME
		show_labels()
		pygame.display.update()
		clock.tick(60)

	pygame.quit()
