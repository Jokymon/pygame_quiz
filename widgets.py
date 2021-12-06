import copy
import pygame
import pygame.gfxdraw
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


class Button(pygame.sprite.Sprite):
    """A pygame GUI button."""
    def __init__(self, position, text,
        theme=style.pyquiz_theme,
        command=None):
        super().__init__()

        self.text = text
        self.style = copy.copy(theme.button)
        self.command = command

        self.set_text(self.text)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.rect.w = 500

    def set_text(self, text):
        self.image = self.style.font.render(text, 1, self.style.normal.text_color)

    def update(self, screen):
        colors = self._current_gui_colors()
        self._draw_button(screen, colors)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.command is not None:
                    self.command()

    def _current_gui_colors(self):
        if self.command is None:
            return self.style.normal
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return self.style.hover
        return self.style.normal

    def _draw_button(self, screen, colors):
        # the width is set to 500 to have the same size not depending on the text size
        pygame.draw.rect(screen, colors.background_color,
            (self.rect.x - 50, self.rect.y, 500 , self.rect.h))
        pygame.gfxdraw.rectangle(screen, (self.rect.x - 50, self.rect.y, 500 , self.rect.h),
            self.style.border_color)