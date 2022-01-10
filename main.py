import os
import sys
import random

import pygame

WIDTH = 1800
HEIGHT = 1000
FPS = 15
SELECTED = False
LEVEL_PURPLE = 1
LEVEL_BLUE = 1
TURN_PLAYER = 1
DIAMETR = 90
BLUE_EXAMS = []
PIGS_BLUE = [1, 1, 1, 1, 1, 1, 1, 1]
PIGS_PURPLE = [1, 1, 1, 1, 1, 1, 1, 1]
IMAGE = ['data/back.jpg', 'data/back1.jpg', 'data/back2.jpg']


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size, color1, color2):

        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.color = [color1, color2]

    def render(self, surface: pygame.Surface):

        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if (row + column) % 2 == 0:
                    pygame.draw.rect(
                        surface=surface,
                        color=self.color[0],
                        rect=(
                            self.left + self.cell_size * column,
                            self.top + self.cell_size * row,
                            self.cell_size,
                            self.cell_size
                        ),
                        width=0
                    )
                else:
                    pygame.draw.rect(
                        surface=surface,
                        color=self.color[1],
                        rect=(
                            self.left + self.cell_size * column,
                            self.top + self.cell_size * row,
                            self.cell_size,
                            self.cell_size
                        ),
                        width=0
                    )
                pygame.draw.rect(
                    surface=surface,
                    color='black',
                    rect=(
                        self.left + self.cell_size * column,
                        self.top + self.cell_size * row,
                        self.cell_size,
                        self.cell_size
                    ),
                    width=1
                )

class Pig_purple(pygame.sprite.Sprite):
    PURPLE = load_image("purple.png")

    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Pig_blue.BLUE, (DIAMETR, DIAMETR))
        self.rect = self.image.get_rect()
        self.rect.x = 525 + 100 * number
        self.rect.y = 85 + 100 * (LEVEL_PURPLE - 1)
        self.number = number
        self.vector = (0, 0)
        self.fast = 0
        self.life = True

    def update(self, types, randomka, *args):
        global SELECTED
        if self.life and types == 0 and (self.rect.x > 1385 or self.rect.x < 525 or self.rect.y < 85 or self.rect.y > 885):
            self.rect.x = WIDTH + DIAMETR
            self.rect.y = HEIGHT + DIAMETR
            PIGS_PURPLE[self.number] = 0
        elif self.life and types == 1 and self.number == randomka:
            pass


class Pig_blue(pygame.sprite.Sprite):
    BLUE = load_image("blue.png")

    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Pig_blue.BLUE, (DIAMETR, DIAMETR))
        self.rect = self.image.get_rect()
        self.rect.x = 525 + 100 * number
        self.rect.y = 785 - 100 * (LEVEL_BLUE - 1)
        self.number = number
        self.vector = (0, 0)
        self.fast = 0
        self.life = True

    def update(self, types, *args):
        global SELECTED
        if self.life and types == 0 and (self.rect.x > 1385 or self.rect.x < 525 or self.rect.y < 85 or self.rect.y > 885):
            self.rect.x = WIDTH + DIAMETR
            self.rect.y = HEIGHT + DIAMETR
            PIGS_BLUE[self.number] = 0
            self.life = False
        elif self.life and types == 1 and self.rect.x <= args[0][0] <= self.rect.x + DIAMETR and \
                args[0][1] <= self.rect.y + DIAMETR <= self.rect.y and SELECTED == False:
            print(self.number)
            SELECTED = True


PURPLE = load_image("purple.png")
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Чапаев')
    randomka = random.randint(0, 7)
    while not PIGS_PURPLE[randomka]:
        randomka = random.randint(0, 7)
    blue_pigs = pygame.sprite.Group()
    all_sprites2 = pygame.sprite.Group()
    blue_pigs.add(Pig_blue(1))
    blue_pigs.add(Pig_blue(2))
    blue_pigs.add(Pig_blue(3))
    blue_pigs.add(Pig_blue(4))
    blue_pigs.add(Pig_blue(5))
    blue_pigs.add(Pig_blue(6))
    blue_pigs.add(Pig_blue(7))
    blue_pigs.add(Pig_blue(0))
    for i in range(8):
        # можно сразу создавать спрайты с указанием группы
        purple = pygame.sprite.Sprite()
        purple.image = pygame.transform.scale(PURPLE, (DIAMETR, DIAMETR))
        purple.rect = purple.image.get_rect()
        # задаём случайное местоположение бомбочке
        purple.rect.x = 525 + 100 * i
        purple.rect.y = 85 + 100 * (LEVEL_PURPLE - 1)
        all_sprites2.add(purple)
    back = pygame.image.load(random.choice(IMAGE))
    back_rect = back.get_rect()
    board = Board(8, 8)
    clock = pygame.time.Clock()
    board.set_view(520, 80, 100, 'white', 'brown')
    running = True
    screen.blit(back, back_rect)
    board.render(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if TURN_PLAYER == 1:
                    blue_pigs.update(1, randomka, event.pos)
        blue_pigs.update(0)
        blue_pigs.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
