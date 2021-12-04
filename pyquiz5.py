import pygame
import pygame.gfxdraw
import random
import themes
from label import *


class Game:
    def __init__(self):
        self.current_question_number = 1
        self.points = 0
        self.questions = [
            ["What is Italy's Capital?", ["Rome", "Paris", "Tokyo", "Madrid"]],
            ["What is France's Capital?", ["Paris", "Rome", "Tokyo", "Madrid"]],
            ["What is England's Capital?", ["London", "Rome", "Tokyo", "Madrid"]],
        ]

    def get_current_title(self):
        return self.questions[self.current_question_number-1][0]

    def get_current_answer(self, index):
        return self.questions[self.current_question_number-1][1][index]

    def number_of_questions(self):
        return len(self.questions)

    def give_answer(self, answer_index):
        if answer_index==0:
            self.points += 1
        self.current_question_number += 1

    def has_ended(self):
        return self.current_question_number > self.number_of_questions()


game = Game()


pygame.init()
pygame.mixer.init()
hit = pygame.mixer.Sound("sounds/hit.wav")
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

buttons = pygame.sprite.Group()


class Button(pygame.sprite.Sprite):
    """A pygame GUI button."""
    def __init__(self, position, text,
        theme=themes.pyquiz_theme,
        command=None):
        super().__init__()

        self.text = text
        self.theme = theme
        self.command = command

        self.render(self.text)
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, 500, self.h)

        buttons.add(self)

    def render(self, text):
        self.text_render = self.theme.button.font.render(text, 1, self.theme.button.normal.text_color)
        self.image = self.text_render

    def update(self, *args):
        if len(args)>0 and args[0]=="event":
            self._handle_event(args[1])
        else:
            colors = self._current_gui_colors()
            self._draw_button(colors)

    def _handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.command is not None:
                    hit.play()
                    print("The answer is:'" + self.text + "'")
                    self.command()

    def _current_gui_colors(self):
        if self.command is None:
            return self.theme.button.normal
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return self.theme.button.hover
        return self.theme.button.normal

    def _draw_button(self, colors):
        # the width is set to 500 to have the same size not depending on the text size
        pygame.draw.rect(screen, colors.background_color,
            (self.x - 50, self.y, 500 , self.h))
        pygame.gfxdraw.rectangle(screen, (self.x - 50, self.y, 500 , self.h),
            self.theme.button.border_color)


def check_score(answer_index):
    """Check for correct answer, update the game state and update the GUI"""
    print(game.current_question_number, game.number_of_questions())

    if game.has_ended():
        return

    game.give_answer(answer_index)

    if not game.has_ended():
        score.change_text(str(game.points))
        title.change_text(game.get_current_title(), color="cyan")
        num_question.change_text(str(game.current_question_number))

        show_question()
    else:
        kill()
        score.change_text("You reached a score of " + str(game.points))


def show_question():
    button1.render(game.get_current_answer(0))
    button2.render(game.get_current_answer(1))
    button3.render(game.get_current_answer(2))
    button4.render(game.get_current_answer(3))


def kill():
    for button in buttons:
        button.kill()


# ================= SOME LABELS ==========================
num_question = Label(screen, str(game.current_question_number), 0, 0)
score = Label(screen, "Punteggio", 50, 300)
title = Label(screen, game.get_current_title(), 10, 10, 55, color="cyan")
write1 = Label(screen, "PYQUIZ BY GiovanniPython", 50, 350, 20, color="red")

Button((10, 100), "1. ")
Button((10, 150), "2. ")
Button((10, 200), "3. ")
Button((10, 250), "4. ")
button1 = Button((50, 100), game.get_current_answer(0),
    command=lambda: check_score(0))
button2 = Button((50, 150), game.get_current_answer(1),
    command=lambda: check_score(1))
button3 = Button((50, 200), game.get_current_answer(2),
    command=lambda: check_score(2))
button4 = Button((50, 250), game.get_current_answer(3),
    command=lambda: check_score(3))


def loop():
    show_question()

    quit = False
    while not quit:
        screen.fill(0)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit = True
            buttons.update("event", event)
        if not quit:
            buttons.update()
            buttons.draw(screen)
            show_labels()
            clock.tick(60)
            pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    loop()