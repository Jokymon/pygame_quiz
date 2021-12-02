import pygame
import pygame.gfxdraw
import time
import random
from label import *


current_question_number = 1
points = 0

pygame.init()
pygame.mixer.init()
hit = pygame.mixer.Sound("sounds/hit.wav")
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

buttons = pygame.sprite.Group()
class Button(pygame.sprite.Sprite):
    ''' A button treated like a Sprite... and killed too '''
    
    def __init__(self, position, text, size,
        colors="white on blue",
        hover_colors="red on green",
        borderc=(255,255,255),
        command=lambda: print("No command activated for this button")):

        # the hover_colors attribute needs to be fixed
        super().__init__()

        self.text = text
        self.command = command
        # --- colors ---
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        # hover_colors
        if hover_colors == "red on green":
            self.hover_colors = f"{self.bg} on {self.fg}"
        else:
            self.hover_colors = hover_colors
        self.borderc = borderc
        # font
        self.font = pygame.font.SysFont("Arial", size)
        self.render(self.text)
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, 500, self.h)
        self.position = position
        self.pressed = 1
        # the groups with all the buttons
        buttons.add(self)

    def render(self, text):
        # we have a surface
        self.text_render = self.font.render(text, 1, self.fg)
        # memorize the surface in the image attributes
        self.image = self.text_render

    def update(self):
        self.fg, self.bg = self.colors.split(" on ")
        self.draw_button()
        if self.command != None:
            self.hover()
            self.click()

    def draw_button(self):
        ''' a linear border '''
        # the width is set to 500 to have the same size not depending on the text size
        pygame.draw.rect(screen, self.bg, (self.x - 50, self.y, 500 , self.h))
        pygame.gfxdraw.rectangle(screen, (self.x - 50, self.y, 500 , self.h), self.borderc)

    def check_collision(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # you can change the colors when the pointer is on the button if you want
            self.colors = self.hover_colors
            # pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            self.colors = self.original_colors
            # pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def hover(self):
        ''' checks if the mouse is over the button and changes the color if it is true '''

        self.check_collision()

    def click(self):
        ''' checks if you click on the button and makes the call to the action just one time'''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                print("The answer is:'" + self.text + "'")
                self.command()
                self.pressed = 0

            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1



# ACTION FOR BUTTON CLICK ================

def on_right():
    check_score("right")


def on_false():
    ''' if there is no 'right' as arg it means it's false '''
    check_score()


def check_score(answered="wrong"):
    ''' here we check if the answer is right '''
    global current_question_number, points
    
    # until there are questions (before last)
    hit.play() # click sound
    if current_question_number < len(questions):
        print(current_question_number, len(questions))
        if answered == "right":
            time.sleep(.1) # to avoid adding more point when pressing too much
            points += 1
            # Show the score text
        current_question_number += 1 # counter for next question in the list
        score.change_text(str(points))
        # Change the text of the question
        title.change_text(questions[current_question_number-1][0], color="cyan")
        # change the question number
        num_question.change_text(str(current_question_number))
        show_question(current_question_number) # delete old buttons and show new
        
    # for the last question...
    elif current_question_number == len(questions):
        print(current_question_number, len(questions))
        if answered == "right":
            kill()
            time.sleep(.1)
            points +=1
        score.change_text("You reached a score of " + str(points))
    time.sleep(.5)


questions = [
    ["What is Italy's Capital?", ["Rome", "Paris", "Tokyo", "Madrid"]],
    ["What is France's Capital?", ["Paris", "Rome", "Tokyo", "Madrid"]],
    ["What is England's Capital?", ["London", "Rome", "Tokyo", "Madrid"]],
]


def show_question(current_question_number):
    # Kills the previous buttons/sprites
    kill()

    button_y_positions = [100, 150, 200, 250]
    # randomized, so that the right one is not on top
    random.shuffle(button_y_positions)

    Button((10, 100), "1. ", 36, "red on yellow",
        hover_colors="blue on orange", borderc=(255,255,0),
        command=None)
    Button((10, 150), "2. ", 36, "red on yellow",
        hover_colors="blue on orange", borderc=(255,255,0),
        command=None)
    Button((10, 200), "3. ", 36, "red on yellow",
        hover_colors="blue on orange", borderc=(255,255,0),
        command=None)
    Button((10, 250), "4. ", 36, "red on yellow",
        hover_colors="blue on orange", borderc=(255,255,0),
        command=None)


    # ============== TEXT: question and answers ====================
    Button((50, button_y_positions[0]), questions[current_question_number-1][1][0], 36, "red on yellow",
        hover_colors="blue on orange", borderc=(255,255,0),
        command=on_right)
    Button((50, button_y_positions[1]), questions[current_question_number-1][1][1], 36, "red on yellow",
        hover_colors="blue on orange", borderc=(255,255,0),
        command=on_false)
    Button((50, button_y_positions[2]), questions[current_question_number-1][1][2], 36, "red on yellow",
        hover_colors="blue on orange", borderc=(255,255,0),
        command=on_false)
    Button((50, button_y_positions[3]), questions[current_question_number-1][1][3], 36, "red on yellow",
        hover_colors="blue on orange", borderc=(255,255,0),
        command=on_false)


def kill():
    for button in buttons:
        button.kill()


# ================= SOME LABELS ==========================
num_question = Label(screen, str(current_question_number), 0, 0)
score = Label(screen, "Punteggio", 50, 300)
title = Label(screen, questions[current_question_number-1][0], 10, 10, 55, color="cyan")
write1 = Label(screen, "PYQUIZ BY GiovanniPython", 50, 350, 20, color="red")

def loop():
    show_question(current_question_number)

    quit = False
    while not quit:
        screen.fill(0)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit = True
        if not quit:
            buttons.update()
            buttons.draw(screen)
            show_labels()        #                 update labels
            clock.tick(60)
            pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    loop()