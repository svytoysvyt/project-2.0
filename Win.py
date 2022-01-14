import pygame
import os

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Размеры окна
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка фонового изображения
win_white_bg = pygame.image.load('win_white_background.jpg')
win_black_bg = pygame.image.load('win_black_background.jpg')


# Рендер текста
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, True, textColor)

    return newText


# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

# Шрифт
font = "opensans.ttf"


def ending_page():
    win_white = False  # Победитель по умолчанию
    win = True
    while win:
        for event in pygame.event.get():  # Заставляем работать крестик
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Текст победителей
        win_white_text = text_format('Победили белые', font, 90, white)
        win_black_text = text_format('Победили чёрные', font, 90, black)

        win_white_rect = win_white_text.get_rect()
        win_black_rect = win_black_text.get_rect()

        if win_white:
            #  Если победили белые рисуем их фон и их текст
            screen.blit(win_white_bg, (0, 0))
            screen.blit(win_white_text, (screen_width / 2 - (win_white_rect[2] / 2), screen_height / 2 - screen_height * 0.2))
        else:
            # И наоборот
            screen.blit(win_black_bg, (0, 0))
            screen.blit(win_black_text,
                        (screen_width / 2 - (win_black_rect[2] / 2), screen_height / 2 - screen_height * 0.2))

        pygame.display.update()


ending_page()
pygame.quit()
quit()
