import pygame


pygame.init()


class Style():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def update(self, style):
        for key, value in style.__dict__.items():
            if isinstance(value, Style):
                self.__dict__[key].update(value)
            else:
                self.__dict__[key] = value


pyquiz_theme = Style(
    button = Style(
        font = pygame.font.SysFont("Arial", 36),
        normal = Style(
            text_color = "red",
            background_color = "yellow"
        ),
        border_color = (255, 255, 0),
        hover = Style(
            text_color = "blue",
            background_color = "orange"
        )
    )
)