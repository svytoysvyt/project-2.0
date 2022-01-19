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
LEVEL_BLACK = 1
LEVEL_WHITE = 1
TURN_PLAYER = 1
RADIUS = 45
PIGS_WHITE = [1, 1, 1, 1, 1, 1, 1, 1]
PIGS_BLACK = [1, 1, 1, 1, 1, 1, 1, 1]
BLACK_cordinat = [1, 1, 1, 1, 1, 1, 1, 1]
WHITE_cordinat = [1, 1, 1, 1, 1, 1, 1, 1]
IMAGE = ['data/back.jpg', 'data/back1.jpg', 'data/back2.jpg']


def load_image(name):
    """
    функция загрузка изображения

    """
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
                    pygame.draw.rect(surface=surface, color=self.color[1], rect=(
                        self.left + self.cell_size * column,
                        self.top + self.cell_size * row,
                        self.cell_size,
                        self.cell_size
                    ))
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


class Pig_black(pygame.sprite.Sprite):
    """
класс черных шашек
    """
    BLACK = load_image("black.png")
    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Pig_black.BLACK, (RADIUS * 2, RADIUS * 2))
        self.rect = self.image.get_rect()
        self.rect.x = 525 + 100 * number
        self.rect.y = 85 + 100 * (LEVEL_BLACK - 1)
        self.number = number
        self.vector = (0, 0)
        self.fast = 0
        BLACK_cordinat[self.number] = [self.rect, self.vector, self.fast]
        self.select = False

    def update(self, types, *args):
        """'работа' этого класса

        :param types:
        тип с которым вызывают этот класс
        :param args:
        меняющиеся переменные
        """
        global SELECTED
        global TURN_PLAYER
        global BLACK_cordinat
        global WHITE_cordinat
        if types == 666:
            self.kill()
        if types == 777:
            self.select = False

        self.fast = BLACK_cordinat[self.number][2]
        self.vector = BLACK_cordinat[self.number][1]
        for i in range(8):
            if i == self.number:
                continue
            x1 = self.rect.x
            y1 = self.rect.y
            x2 = BLACK_cordinat[i][0][0]
            y2 = BLACK_cordinat[i][0][1]
            dx1 = self.vector[0]
            dy1 = self.vector[1]
            dx2 = BLACK_cordinat[i][1][0]
            dy2 = BLACK_cordinat[i][1][1]
            Dx = (x1 - x2)
            Dy = (y1 - y2)
            d = (Dx ** 2 + Dy ** 2) ** 0.5
            if d == 0:
                d = 0.01
            s = Dx / d
            e = Dy / d
            if d <= 2 * RADIUS:
                Vn1 = dx2 * s + dy2 * e
                Vn2 = dx1 * s + dy1 * e
                dt = (2 * RADIUS - d) / (Vn1 - Vn2)
                if dt > 0.6:
                    dt = 0.6
                elif dt < -0.6:
                    dt = -0.6
                self.rect.x -= dx1 * dt
                self.rect.y -= dy1 * dt
                x2 -= dx2 * dt
                y2 -= dy2 * dt
                Dx = (x1 - x2)
                Dy = (y1 - y2)
                d = (Dx ** 2 + Dy ** 2) ** 0.5
                if d == 0:
                    d = 0.01
                s = Dx / d
                e = Dy / d
                Vn1 = dx2 * s + dy2 * e
                Vn2 = dx1 * s + dy1 * e
                Vt1 = -dx2 * e + dy2 * s
                Vt2 = -dx1 * e + dy1 * s

                o = Vn2
                Vn2 = Vn1
                Vn1 = o
                self.fast = (self.fast + BLACK_cordinat[i][2]) / 2
                if self.fast < 0:
                    self.fast = 0
                BLACK_cordinat[i][2] = self.fast
                self.vector = (Vn2 * s - Vt2 * e, Vn2 * e + Vt2 * s)
                BLACK_cordinat[i][1] = (Vn1 * s - Vt1 * e, Vn1 * e + Vt1 * s)
        for i in range(8):
            x1 = self.rect.x
            y1 = self.rect.y
            x2 = WHITE_cordinat[i][0][0]
            y2 = WHITE_cordinat[i][0][1]
            dx1 = self.vector[0]
            dy1 = self.vector[1]
            dx2 = WHITE_cordinat[i][1][0]
            dy2 = WHITE_cordinat[i][1][1]
            Dx = (x1 - x2)
            Dy = (y1 - y2)
            d = (Dx ** 2 + Dy ** 2) ** 0.5
            if d == 0:
                d = 0.01
            s = Dx / d
            e = Dy / d
            if d <= 2 * RADIUS:
                Vn1 = dx2 * s + dy2 * e
                Vn2 = dx1 * s + dy1 * e
                dt = (2 * RADIUS - d) / (Vn1 - Vn2)
                if dt > 0.6:
                    dt = 0.6
                elif dt < -0.6:
                    dt = -0.6
                self.rect.x -= dx1 * dt
                self.rect.y -= dy1 * dt
                x2 -= dx2 * dt
                y2 -= dy2 * dt
                Dx = (x1 - x2)
                Dy = (y1 - y2)
                d = (Dx ** 2 + Dy ** 2) ** 0.5
                if d == 0:
                    d = 0.01
                s = Dx / d
                e = Dy / d
                Vn1 = dx2 * s + dy2 * e
                Vn2 = dx1 * s + dy1 * e
                Vt1 = -dx2 * e + dy2 * s
                Vt2 = -dx1 * e + dy1 * s

                o = Vn2
                Vn2 = Vn1
                Vn1 = o
                self.fast = (self.fast + WHITE_cordinat[i][2]) / 2
                if self.fast < 0:
                    self.fast = 0
                WHITE_cordinat[i][2] = self.fast
                self.vector = (Vn2 * s - Vt2 * e, Vn2 * e + Vt2 * s)
                WHITE_cordinat[i][1] = (Vn1 * s - Vt1 * e, Vn1 * e + Vt1 * s)
        if types == 0 and (self.rect.x + RADIUS > 1320 or self.rect.x + RADIUS < 520 or
                           self.rect.y + RADIUS < 80 or self.rect.y + RADIUS > 880):
            self.rect.x = WIDTH
            self.rect.y = HEIGHT
            PIGS_BLACK[self.number] = 0
            BLACK_cordinat[self.number][2] = 0
            if all(x[2] == 0 for x in BLACK_cordinat) and all(x[2] == 0 for x in WHITE_cordinat)\
                    and (TURN_PLAYER == 2 or TURN_PLAYER == 3):
                if TURN_PLAYER == 2:
                    TURN_PLAYER = 0
                else:
                    TURN_PLAYER = 1
                SELECTED = False
                black_pigs.update(777)
                whire_pigs.update(777)

            self.kill()
        elif types == 1 and self.number == args[0] and not SELECTED:
            self.select = True
            SELECTED = True
            LEN = ((self.rect.x - args[1][0]) ** 2 + (self.rect.y - args[1][1]) ** 2) ** 0.5
            self.vector = (110 * (args[1][0] - self.rect.x) / LEN,
                           110 * (args[1][1] - self.rect.y) / LEN)

            self.fast = ((self.vector[0]) ** 2 + (self.vector[1]) ** 2) ** 0.5 // 2
            print(self.vector, self.fast, 898989889)
            TURN_PLAYER = 3

        elif (TURN_PLAYER == 3 or TURN_PLAYER == 2) and self.fast != 0:
            if self.fast > 0:
                self.fast -= 2.2
                self.rect = self.rect.move(self.vector[0] * self.fast // 100, self.vector[1] * self.fast // 100)

            else:
                self.fast = 0

            BLACK_cordinat[self.number][2] = self.fast
            if all(x[2] == 0 for x in BLACK_cordinat) and all(x[2] == 0 for x in WHITE_cordinat):
                if TURN_PLAYER == 2:
                    TURN_PLAYER = 0
                else:
                    TURN_PLAYER = 1
                SELECTED = False
                black_pigs.update(777)
                whire_pigs.update(777)
        BLACK_cordinat[self.number] = [self.rect, self.vector, self.fast]

#           if pygame.sprite.spritecollideany(self, horizontal_borders):
#              self.vector[0] *= -1
#            if pygame.sprite.spritecollideany(self, vertical_borders):
#               self.vector[1] *= -1


class Pig_white(pygame.sprite.Sprite):
    """

    """
    WHITE = load_image("white.png")

    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Pig_white.WHITE, (RADIUS * 2, RADIUS * 2))
        self.rect = self.image.get_rect()
        self.rect.x = 525 + 100 * number
        self.rect.y = 785 - 100 * (LEVEL_WHITE - 1)
        self.number = number
        self.vector = (0, 0)
        self.fast = 0
        WHITE_cordinat[self.number] = [self.rect, self.vector, self.fast]
        self.select = False
        PIGS_WHITE[self.number] = (self.rect.x + RADIUS, self.rect.y + RADIUS)

    def update(self, types, *args):
        global SELECTED
        global RADIUS
        global TURN_PLAYER
        if types == 666:
            self.kill()
        if types == 777:
            self.select = False
        self.vector = WHITE_cordinat[self.number][1]
        self.fast = WHITE_cordinat[self.number][2]
        for i in range(8):
            x1 = self.rect.x
            y1 = self.rect.y
            x2 = BLACK_cordinat[i][0][0]
            y2 = BLACK_cordinat[i][0][1]
            dx1 = self.vector[0]
            dy1 = self.vector[1]
            dx2 = BLACK_cordinat[i][1][0]
            dy2 = BLACK_cordinat[i][1][1]
            Dx = (x1 - x2)
            Dy = (y1 - y2)
            d = (Dx ** 2 + Dy ** 2) ** 0.5
            if d == 0:
                d = 0.01
            s = Dx / d
            e = Dy / d
            if d <= 2 * RADIUS:
                Vn1 = dx2 * s + dy2 * e
                Vn2 = dx1 * s + dy1 * e
                dt = (2 * RADIUS - d) / (Vn1 - Vn2)

                if dt > 0.6:
                    dt = 0.6
                elif dt < -0.6:
                    dt = -0.6
                self.rect.x -= dx1 * dt
                self.rect.y -= dy1 * dt
                x2 -= dx2 * dt
                y2 -= dy2 * dt
                Dx = (x1 - x2)
                Dy = (y1 - y2)
                d = (Dx ** 2 + Dy ** 2) ** 0.5
                if d == 0:
                    d = 0.01
                s = Dx / d
                e = Dy / d
                Vn1 = dx2 * s + dy2 * e
                Vn2 = dx1 * s + dy1 * e
                Vt1 = -dx2 * e + dy2 * s
                Vt2 = -dx1 * e + dy1 * s

                o = Vn2
                Vn2 = Vn1
                Vn1 = o
                self.fast = (self.fast + BLACK_cordinat[i][2]) / 2
                BLACK_cordinat[i][2] = self.fast
                if self.fast < 0:
                    self.fast = 0
                if BLACK_cordinat[i][2] < 0:
                    BLACK_cordinat[i][2] = 0
                self.vector = (Vn2 * s - Vt2 * e, Vn2 * e + Vt2 * s)
                BLACK_cordinat[i][1] = (Vn1 * s - Vt1 * e, Vn1 * e + Vt1 * s)
        for i in range(8):
            if i == self.number:
                continue
            x1 = self.rect.x
            y1 = self.rect.y
            x2 = WHITE_cordinat[i][0][0]
            y2 = WHITE_cordinat[i][0][1]
            dx1 = self.vector[0]
            dy1 = self.vector[1]
            dx2 = WHITE_cordinat[i][1][0]
            dy2 = WHITE_cordinat[i][1][1]
            Dx = (x1 - x2)
            Dy = (y1 - y2)
            d = (Dx ** 2 + Dy ** 2) ** 0.5
            if d == 0:
                d = 0.01
            s = Dx / d
            e = Dy / d
            if d <= 2 * RADIUS:
                Vn1 = dx2 * s + dy2 * e
                Vn2 = dx1 * s + dy1 * e
                dt = (2 * RADIUS - d) / (Vn1 - Vn2)

                if dt > 0.6:
                    dt = 0.6
                elif dt < -0.6:
                    dt = -0.6
                self.rect.x -= dx1 * dt
                self.rect.y -= dy1 * dt
                x2 -= dx2 * dt
                y2 -= dy2 * dt
                Dx = (x1 - x2)
                Dy = (y1 - y2)
                d = (Dx ** 2 + Dy ** 2) ** 0.5
                if d == 0:
                    d = 0.01
                s = Dx / d
                e = Dy / d
                Vn1 = dx2 * s + dy2 * e
                Vn2 = dx1 * s + dy1 * e
                Vt1 = -dx2 * e + dy2 * s
                Vt2 = -dx1 * e + dy1 * s

                o = Vn2
                Vn2 = Vn1
                Vn1 = o
                self.vector = (Vn2 * s - Vt2 * e, Vn2 * e + Vt2 * s)
                self.fast = (self.fast + WHITE_cordinat[i][2]) / 2
                if self.fast < 0:
                    self.fast = 0
                WHITE_cordinat[i][1] = (Vn1 * s - Vt1 * e, Vn1 * e + Vt1 * s)
                WHITE_cordinat[i][2] = (self.fast + WHITE_cordinat[i][2]) / 2
        if types == 2 and self.select:
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
            WHITE_cordinat[self.number][2] = self.fast
        if (TURN_PLAYER == 2 or TURN_PLAYER == 3) and self.fast:
            WHITE_cordinat[self.number][2] = self.fast
            if self.fast > 0:
                self.fast -= 2.2
                print(self.fast, self.vector, 'kkk')
                self.rect = self.rect.move(self.vector[0] * self.fast // 100, self.vector[1] * self.fast // 100)
            else:
                self.fast = 0
            WHITE_cordinat[self.number][2] = self.fast
            print('er', TURN_PLAYER, self.number)
            for i in WHITE_cordinat:
                print(i[2])
            print('y')
            for i in BLACK_cordinat:
                print(i[2])
            print('uu')
            if all(x[2] == 0 for x in BLACK_cordinat) and all(x[2] == 0 for x in WHITE_cordinat):
                if TURN_PLAYER == 2:
                    TURN_PLAYER = 0
                else:
                    TURN_PLAYER = 1
                SELECTED = False
                black_pigs.update(777)
                whire_pigs.update(777)  
        PIGS_WHITE[self.number] = (self.rect.x + RADIUS, self.rect.y + RADIUS)
        if types == 0 and (self.rect.x + RADIUS > 1320 or self.rect.x + RADIUS < 520 or
                           self.rect.y + RADIUS < 80 or self.rect.y + RADIUS > 880):
            PIGS_WHITE[self.number] = 0
            WHITE_cordinat[self.number][2] = 0
            if all(x[2] == 0 for x in BLACK_cordinat) and all(x[2] == 0 for x in WHITE_cordinat)\
                    and (TURN_PLAYER == 2 or TURN_PLAYER == 3):
                if TURN_PLAYER == 2:
                    TURN_PLAYER = 0
                else:
                    TURN_PLAYER = 1
                SELECTED = False
                black_pigs.update(777)
                whire_pigs.update(777)

            self.kill()
        WHITE_cordinat[self.number] = [self.rect, self.vector, self.fast]


if __name__ == '__main__':
    pygame.display.set_caption('Чапаев')
    whire_pigs = pygame.sprite.Group()
    black_pigs = pygame.sprite.Group()
    for i in range(8):
        whire_pigs.add(Pig_white(i))
        black_pigs.add(Pig_black(i))
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
        whire_pigs.draw(screen)
        black_pigs.draw(screen)
        black_pigs.update(0)
        whire_pigs.update(0)
        if not all(x == 0 for x in PIGS_WHITE) and all(x == 0 for x in PIGS_BLACK):
            if LEVEL_WHITE + LEVEL_BLACK == 8:
                LEVEL_BLACK -= 1
            else:
                LEVEL_WHITE += 1
            black_pigs.update(666)
            whire_pigs.update(666)
            SELECTED = False
            TURN_PLAYER = 1
            WHITE_cordinat = [0, 0, 0, 0, 0, 0, 0, 0]
            BLACK_cordinat = [0, 0, 0, 0, 0, 0, 0, 0]
            PIGS_WHITE = [1, 1, 1, 1, 1, 1, 1, 1]
            PIGS_BLACK = [1, 1, 1, 1, 1, 1, 1, 1]
            for i in range(8):
                whire_pigs.add(Pig_white(i))
                black_pigs.add(Pig_black(i))
        elif all(x == 0 for x in PIGS_WHITE) and not all(x == 0 for x in PIGS_BLACK):
            if LEVEL_WHITE + LEVEL_BLACK == 8:
                LEVEL_WHITE -= 1
            else:
                LEVEL_BLACK += 1
            black_pigs.update(666)
            whire_pigs.update(666)
            SELECTED = False
            TURN_PLAYER = 1
            WHITE_cordinat = [0, 0, 0, 0, 0, 0, 0, 0]
            BLACK_cordinat = [0, 0, 0, 0, 0, 0, 0, 0]
            PIGS_WHITE = [1, 1, 1, 1, 1, 1, 1, 1]
            PIGS_BLACK = [1, 1, 1, 1, 1, 1, 1, 1]

            for i in range(8):
                whire_pigs.add(Pig_white(i))
                black_pigs.add(Pig_black(i))
        elif all(x == 0 for x in PIGS_WHITE) and all(x == 0 for x in PIGS_BLACK):
            black_pigs.update(666)
            whire_pigs.update(666)
            SELECTED = False
            TURN_PLAYER = 1
            WHITE_cordinat = [0, 0, 0, 0, 0, 0, 0, 0]
            BLACK_cordinat = [0, 0, 0, 0, 0, 0, 0, 0]
            PIGS_WHITE = [1, 1, 1, 1, 1, 1, 1, 1]
            PIGS_BLACK = [1, 1, 1, 1, 1, 1, 1, 1]
            for i in range(8):
                whire_pigs.add(Pig_white(i))
                black_pigs.add(Pig_black(i))
        randomka_white = random.randint(0, 7)
        while not PIGS_WHITE[randomka_white]:
            randomka_white = random.randint(0, 7)
        randomka_black = random.randint(0, 7)
        while not PIGS_BLACK[randomka_black]:
            randomka_black = random.randint(0, 7)
        randomka_white = PIGS_WHITE[randomka_white]
        if TURN_PLAYER == 1 and SELECTED:
            whire_pigs.update(2, pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and SELECTED and TURN_PLAYER == 1:
                whire_pigs.update(3, event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and TURN_PLAYER == 1 and not SELECTED:
                whire_pigs.update(1, event.pos)
            if TURN_PLAYER == 0:
                black_pigs.update(1, randomka_black, randomka_white)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
