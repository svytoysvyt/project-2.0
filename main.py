import os
import sys
import random

import pygame
FPS = 15
LEVEL_PURPLE = 1
LEVEL_BLUE = 1
TURN_PLAYER = True

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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
                if (row+column) % 2 == 0:
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


class Pig_blue(pygame.sprite.Sprite):
    BLUE = load_image("blue.png")

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(Pig_blue.BLUE, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = 525 + 100 * i
        self.rect.y = 785 - 100 * (LEVEL_BLUE - 1)
        self.selected = False

        def select(self, *args, **kwargs):


        def update(self):
            if self.rect.x > 1385 or self.rect.x < 525 or self.rect.y < 85 or self.rect.y > 885:






PURPLE = load_image("purple.png")
IMAGE = ['data/back.jpg', 'data/back1.jpg', 'data/back2.jpg']
if __name__ == '__main__':
    pygame.init()
    screen = pygame.Surface((1800, 950))
    pygame.display.set_caption('чапаев')
    all_sprites1 = pygame.sprite.Group()
    all_sprites2 = pygame.sprite.Group()
    for i in range(8):
        # можно сразу создавать спрайты с указанием группы


        purple = pygame.sprite.Sprite()
        purple.image = pygame.transform.scale(PURPLE, (90, 90))
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
    all_sprites1.draw(screen)
    all_sprites2.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
