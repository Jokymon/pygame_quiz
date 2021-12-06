import pygame
import pygame.gfxdraw
import random
import themes
from label import *


class Game:
    def __init__(self):
        self.current_question_number = 0
        self.points = 0
        self.questions = [
            ["What is Italy's Capital?", ["Rome", "Paris", "Tokyo", "Madrid"]],
            ["What is France's Capital?", ["Paris", "Rome", "Tokyo", "Madrid"]],
            ["What is England's Capital?", ["London", "Rome", "Tokyo", "Madrid"]],
        ]
        self._next_question()

    def get_current_title(self):
        return self.questions[self.current_question_number-1][0]

    def get_current_answer(self, index):
        return self.current_answers[index]

    def number_of_questions(self):
        return len(self.questions)

    def give_answer(self, answer_index):
        if answer_index==self.current_correct_index:
            self.points += 1
        if not self.has_ended():
            self._next_question()

    def has_ended(self):
        return self.current_question_number > self.number_of_questions()

    def _next_question(self):
        self.current_question_number += 1
        if self.has_ended():
            return

        # We know that the correct answer is always at index 0; so we create a new
        # list where every entry consists of a pair of index and entry:
        # [ (0, "answer 1"), (1, "answer 2"), .... ]
        # When we shuffle this list, we now have to extract at which position the
        # index 0-entry has now landed. This position gives us the index of the
        # correct answer.
        # [ (1, "answer 2"), (2, "answer 3"), (0, "answer 1") ]
        # In this example, the correct answer (answer 1) landed on index 2. Using
        # the .index()-function on entry '0' we find that index.
        current_answers = self.questions[self.current_question_number-1][1]
        indexed_answers = list(zip(range(len(current_answers)), current_answers))

        random.shuffle(indexed_answers)

        indices, current_answers = zip(*indexed_answers)
        self.current_answers = current_answers
        self.current_correct_index = indices.index(0)


pygame.init()
pygame.mixer.init()
hit = pygame.mixer.Sound("sounds/hit.wav")
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()


class Button(pygame.sprite.Sprite):
    """A pygame GUI button."""
    def __init__(self, position, text,
        theme=themes.pyquiz_theme,
        command=None):
        super().__init__()

        self.text = text
        self.theme = theme
        self.command = command

        self.set_text(self.text)
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, 500, self.h)

    def set_text(self, text):
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


class Ui:
    def __init__(self, game):
        self.game = game
        self.buttons = pygame.sprite.Group()
        self.labels = pygame.sprite.Group()

        self.num_question = Label(screen, f"Question {self.game.current_question_number}:", 10, 10, 30)
        self.labels.add(self.num_question)
        self.title = Label(screen, self.game.get_current_title(), 10, 40, 30, color="cyan")
        self.labels.add(self.title)
        self.score = Label(screen, "Score: 0", 50, 320, 30)
        self.labels.add(self.score)

        self.buttons.add(Button((10, 100), "1. "))
        self.buttons.add(Button((10, 150), "2. "))
        self.buttons.add(Button((10, 200), "3. "))
        self.buttons.add(Button((10, 250), "4. "))
        self.button1 = Button((50, 100), game.get_current_answer(0),
            command=lambda: self.check_score(0))
        self.buttons.add(self.button1)
        self.button2 = Button((50, 150), game.get_current_answer(1),
            command=lambda: self.check_score(1))
        self.buttons.add(self.button2)
        self.button3 = Button((50, 200), game.get_current_answer(2),
            command=lambda: self.check_score(2))
        self.buttons.add(self.button3)
        self.button4 = Button((50, 250), game.get_current_answer(3),
            command=lambda: self.check_score(3))
        self.buttons.add(self.button4)

        self._show_question()

    def handle_event(self, event):
        self.buttons.update("event", event)

    def update(self):
        self.buttons.update()

    def draw(self, screen):
        self.buttons.draw(screen)
        self.labels.draw(screen)

    def check_score(self, answer_index):
        """Check for correct answer, update the game state and update the GUI"""
        print(self.game.current_question_number, self.game.number_of_questions())

        if self.game.has_ended():
            return

        self.game.give_answer(answer_index)

        if not self.game.has_ended():
            self.score.change_text(f"Score: {self.game.points}")
            self.title.change_text(self.game.get_current_title(), color="cyan")
            self.num_question.change_text(f"Question {self.game.current_question_number}:")

            self._show_question()
        else:
            self.kill()
            self.score.change_text(f"You reached a score of {self.game.points}")

    def _show_question(self):
        self.button1.set_text(self.game.get_current_answer(0))
        self.button2.set_text(self.game.get_current_answer(1))
        self.button3.set_text(self.game.get_current_answer(2))
        self.button4.set_text(self.game.get_current_answer(3))

    def kill(self):
        for button in self.buttons:
            button.kill()


def loop():
    game = Game()
    ui = Ui(game)

    quit = False
    while not quit:
        screen.fill(0)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit = True
            ui.handle_event(event)
        if not quit:
            ui.update()
            ui.draw(screen)
            clock.tick(60)
            pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    loop()