class Theme():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


pyquiz_theme = Theme(
    button = Theme(
        normal = Theme(
            text_color = "red",
            background_color = "yellow"
        ),
        border_color = (255, 255, 0),
        hover = Theme(
            text_color = "blue",
            background_color = "orange"
        )
    )
)