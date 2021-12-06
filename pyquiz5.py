import pygame
import random
import style
from widgets import *


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


class Ui:
    def __init__(self, game):
        self.game = game
        self.buttons = pygame.sprite.Group()
        self.labels = pygame.sprite.Group()

        self.hit_sound = pygame.mixer.Sound("sounds/hit.wav")

        self.num_question = Label((10, 10), f"Question {self.game.current_question_number}:")
        self.title = Label((10, 40), self.game.get_current_title(), style=style.Style(text_color="cyan"))
        self.score = Label((50, 320), "Score: 0")
        self.labels.add(self.num_question)
        self.labels.add(self.title)
        self.labels.add(self.score)

        self.buttons.add(Button((10, 100), "1. "))
        self.buttons.add(Button((10, 150), "2. "))
        self.buttons.add(Button((10, 200), "3. "))
        self.buttons.add(Button((10, 250), "4. "))
        self.button1 = Button((50, 100), game.get_current_answer(0),
            command=lambda: self._click_answer(0))
        self.button2 = Button((50, 150), game.get_current_answer(1),
            command=lambda: self._click_answer(1))
        self.button3 = Button((50, 200), game.get_current_answer(2),
            command=lambda: self._click_answer(2))
        self.button4 = Button((50, 250), game.get_current_answer(3),
            command=lambda: self._click_answer(3))
        self.buttons.add(self.button1)
        self.buttons.add(self.button2)
        self.buttons.add(self.button3)
        self.buttons.add(self.button4)

        self._show_question()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self, screen):
        self.buttons.update(screen)

    def draw(self, screen):
        self.buttons.draw(screen)
        self.labels.draw(screen)

    def _click_answer(self, answer_index):
        self.hit_sound.play()
        self._check_score(answer_index)

    def _check_score(self, answer_index):
        """Check for correct answer, update the game state and update the GUI"""
        if self.game.has_ended():
            return

        self.game.give_answer(answer_index)

        if self.game.has_ended():
            self._show_final_result()
        else:
            self.score.set_text(f"Score: {self.game.points}")
            self._show_question()

    def _show_question(self):
        self.title.set_text_color("cyan")
        self.title.set_text(self.game.get_current_title())
        self.num_question.set_text(f"Question {self.game.current_question_number}:")

        self.button1.set_text(self.game.get_current_answer(0))
        self.button2.set_text(self.game.get_current_answer(1))
        self.button3.set_text(self.game.get_current_answer(2))
        self.button4.set_text(self.game.get_current_answer(3))

    def _show_final_result(self):
        for button in self.buttons:
            button.kill()
        self.score.set_text(f"You reached a score of {self.game.points}")


def loop():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()

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
            ui.update(screen)
            ui.draw(screen)
            clock.tick(60)
            pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    loop()