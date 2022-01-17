import os
import sys
import random

import pygame

WIDTH = 1800
HEIGHT = 1000
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 40
SELECTED = False
LEVEL_PURPLE = 1
LEVEL_BLUE = 1
TURN_PLAYER = 1
RADIUS = 45
FASTB = [0, 0, 0, 0, 0, 0, 0, 0]
FASTP = [0, 0, 0, 0, 0, 0, 0, 0]
PIGS_BLUE = [1, 1, 1, 1, 1, 1, 1, 1]
PIGS_PURPLE = [1, 1, 1, 1, 1, 1, 1, 1]
IMAGE = ['data/back.jpg', 'data/back1.jpg', 'data/back2.jpg']


def main_pigs():
    SELECTED = False
    TURN_PLAYER = 1
    PIGS_BLUE = [1, 1, 1, 1, 1, 1, 1, 1]
    PIGS_PURPLE = [1, 1, 1, 1, 1, 1, 1, 1]


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
    PURPLE = load_image("black.png")

    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Pig_purple.PURPLE, (RADIUS * 2, RADIUS * 2))
        self.rect = self.image.get_rect()
        self.rect.x = 525 + 100 * number
        self.rect.y = 85 + 100 * (LEVEL_PURPLE - 1)
        self.number = number
        self.vector = (0, 0)
        self.fast = 0
        self.select = False

    def update(self, types, *args):
        global SELECTED
        global TURN_PLAYER

        #       if pygame.sprite.spritecollideany(self, horizontal_borders):
        #          self.vy = -self.vy
        #     if pygame.sprite.spritecollideany(self, vertical_borders):
        #        self.vx = -self.vx
        if types == 0 and (
                self.rect.x > 1385 or self.rect.x < 525 or self.rect.y < 85 or self.rect.y > 885):
            self.rect.x = WIDTH
            self.rect.y = HEIGHT
            PIGS_PURPLE[self.number] = 0
            self.kill()
        elif types == 1 and self.number == args[0] and not self.select:
            self.select = True
            SELECTED = True
            print(1737371, args)
            LEN = ((self.rect.x - args[1][0]) ** 2 + (self.rect.y - args[1][1]) ** 2) ** 0.5
            self.vector = (110 * (args[1][0] - self.rect.x) / LEN,
                           110 * (args[1][1] - self.rect.y) / LEN)

            self.fast = ((self.vector[0]) ** 2 + (self.vector[1]) ** 2) ** 0.5 // 2
            print(self.vector, self.fast, 898989889)
            TURN_PLAYER = 3

        elif (TURN_PLAYER == 3 or TURN_PLAYER == 2) and self.fast:
            print((self.vector[0] * self.fast // 1000, self.vector[1] * self.fast // 1000), 'pppooioiuui')
            FASTP[self.number] = self.fast
            if self.fast > 0:
                self.fast -= 2.2
                self.rect = self.rect.move(self.vector[0] * self.fast // 100, self.vector[1] * self.fast // 100)

            else:
                self.fast = 0
            FASTP[self.number] = self.fast
            if all(x == 0 for x in FASTP) and all(x == 0 for x in FASTB):
                if TURN_PLAYER == 2:
                    TURN_PLAYER = 0
                else:
                    TURN_PLAYER = 1
                SELECTED = False
                self.select = False


#           if pygame.sprite.spritecollideany(self, horizontal_borders):
#              self.vector[0] *= -1
#            if pygame.sprite.spritecollideany(self, vertical_borders):
#               self.vector[1] *= -1


class Pig_blue(pygame.sprite.Sprite):
    BLUE = load_image("white.png")

    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Pig_blue.BLUE, (RADIUS * 2, RADIUS * 2))
        self.rect = self.image.get_rect()
        self.rect.x = 525 + 100 * number
        self.rect.y = 785 - 100 * (LEVEL_BLUE - 1)
        self.number = number
        self.vector = (0, 0)
        self.fast = 0
        self.select = False
        PIGS_BLUE[self.number] = (self.rect.x + RADIUS, self.rect.y + RADIUS)

    def update(self, types, *args):
        global SELECTED
        global RADIUS
        global TURN_PLAYER
        if types == 2 and self.select:
            print('jhgfde')
            LEN = ((self.rect.x + RADIUS - args[0][0]) ** 2 + (self.rect.y + RADIUS - args[0][1]) ** 2) ** 0.5
            if LEN <= RADIUS * 2.5:
                self.vector = (args[0][0], args[0][1])
            elif RADIUS * 2.5 < LEN:
                self.vector = (2.5 * RADIUS * (args[0][0] - self.rect.x - RADIUS) / LEN + self.rect.x + RADIUS,
                               2.5 * RADIUS * (args[0][1] - self.rect.y - RADIUS) / LEN + self.rect.y + RADIUS)
            pygame.draw.line(screen, (50, 18, 122), [self.rect.x + RADIUS, self.rect.y + RADIUS],
                             [self.vector[0], self.vector[1]], 6)
            pygame.draw.line(screen, (102, 0, 255), [self.rect.x + RADIUS, self.rect.y + RADIUS],
                             [self.vector[0], self.vector[1]], 2)
        elif types == 1 and ((self.rect.x + RADIUS - args[0][0]) ** 2 +
                             (self.rect.y + RADIUS - args[0][1]) ** 2) <= RADIUS ** 2 and not SELECTED:
            print(self.number)
            SELECTED = True
            self.select = True
        elif types == 3 and self.select:
            self.vector = (RADIUS - self.vector[0] + self.rect.x, - self.vector[1] + self.rect.y + RADIUS)
            print('hjjkfffkklklk')
            self.fast = ((self.vector[0]) ** 2 + (self.vector[1]) ** 2) ** 0.5 // 2
            TURN_PLAYER = 2
            FASTB[self.number] = self.fast
        if (TURN_PLAYER == 2 or TURN_PLAYER == 3) and self.fast:
            FASTB[self.number] = self.fast
            if self.fast > 0:
                self.fast -= 2.2
                print(self.fast, self.vector, 'kkk')
                self.rect = self.rect.move(self.vector[0] * self.fast // 100, self.vector[1] * self.fast // 100)
            else:
                print(self.fast, FASTB)
                self.fast = 0
            FASTB[self.number] = self.fast
            if all(x == 0 for x in FASTB) and all(x == 0 for x in FASTP):
                if TURN_PLAYER == 2:
                    TURN_PLAYER = 0
                else:
                    TURN_PLAYER = 1
                self.fast = 0
                SELECTED = False
                self.select = False
        PIGS_BLUE[self.number] = (self.rect.x + RADIUS, self.rect.y + RADIUS)
        if types == 0 and (self.rect.x + RADIUS > 1385 or self.rect.x + RADIUS < 525 or
                           self.rect.y + RADIUS < 85 or self.rect.y + RADIUS > 885):
            PIGS_BLUE[self.number] = 0
            print(767676)
            FASTB[self.number] = 0
            SELECTED = False
            self.kill()



PURPLE = load_image("purple.png")


def main():
    pygame.display.set_caption('Чапаев')
    blue_pigs = pygame.sprite.Group()
    purple_pigs = pygame.sprite.Group()
    for i in range(8):
        blue_pigs.add(Pig_blue(i))
        purple_pigs.add(Pig_purple(i))
    back = pygame.image.load(random.choice(IMAGE))
    back_rect = back.get_rect()
    board = Board(8, 8)
    clock = pygame.time.Clock()
    board.set_view(520, 80, 100, 'white', 'brown')
    running = True
    screen.blit(back, back_rect)
    board.render(screen)
    while running:
        screen.blit(back, back_rect)
        board.render(screen)
        blue_pigs.draw(screen)
        purple_pigs.draw(screen)
        purple_pigs.update(0)
        blue_pigs.update(0)
        randomka_blue = random.randint(0, 7)
        while not PIGS_BLUE[randomka_blue]:
            randomka_blue = random.randint(0, 7)
        randomka_purple = random.randint(0, 7)
        while not PIGS_PURPLE[randomka_purple]:
            randomka_purple = random.randint(0, 7)
        randomka_blue = PIGS_BLUE[randomka_blue]
        if TURN_PLAYER == 1 and SELECTED:
            blue_pigs.update(2, pygame.mouse.get_pos())
        # if TURN_PLAYER == 2:
        #     blue_pigs.update(2, pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and SELECTED and TURN_PLAYER == 1:
                blue_pigs.update(3, event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and TURN_PLAYER == 1 and not SELECTED:
                blue_pigs.update(1, event.pos)
            if TURN_PLAYER == 0:
                purple_pigs.update(1, randomka_purple, randomka_blue)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


main()
