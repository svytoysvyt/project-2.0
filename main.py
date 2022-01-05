import os
import sys

import pygame
FPS = 15


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size, color1, color2, color3):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.color = [color1, color2, color3]

    def render(self, surface: pygame.Surface):
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if (row+column)%2==0:
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


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


image = load_image("back.jpg")

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    board = Board(8, 8)
    clock = pygame.time.Clock()
    board.set_view(70, 70, 70, 'white', 'brown', 'gray')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()