import pygame
import os
import game
pygame.init()

# Переменная отвечающая за обновление экрана
update = True

btn = True
# Центрирование игрового окна
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Размеры окна
screen_width = 1800
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка фонового изображения
bg_menu = pygame.image.load("background_image_menu.jpg")
# Загрузка фонового изображения правил
bg_rules = pygame.image.load('background_image_rules.jpg')


# Рендер текста
def text_format(message, textfont, textsize, textcolor):
    newfont = pygame.font.Font(textfont, textsize)
    newtext = newfont.render(message, True, textcolor)

    return newtext


# Цвет
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

# Шрифт
font = "opensans.ttf"


def main_menu():
    global update
    rules_wind = False
    menu = True
    selected = ''  # Выбранный пункт меню

    while menu:

        screen.blit(bg_menu, (0, 0))
        title = text_format('Чапаев', font, 90, yellow)  # Заголовок
        if selected == "start":
            text_start = text_format("Старт", font, 65, white)  # Меняем стиль кнопки если мышь наведена на неё
        else:
            text_start = text_format("Старт", font, 65, black)  # Стиль кнопки
        if selected == "rules":
            text_rules = text_format("Правила", font, 65, white)  # Меняем стиль кнопки если мышь наведена на неё
        else:
            text_rules = text_format("Правила", font, 65, black)  # Стиль кнопки
        if selected == "quit":
            text_quit = text_format("Выход", font, 65, white)  # Меняем стиль кнопки если мышь наведена на неё
        else:
            text_quit = text_format("Выход", font, 65, black)  # Стиль кнопки

        title_rect = title.get_rect()
        rules_rect = text_rules.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Отрисовываем заголовок (название игры)
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), screen_height / 2 - screen_height * 0.35))

        start_pos = screen.blit(text_start, (screen_width / 2 - (start_rect[2] / 2),
                                        screen_height / 2 - screen_height * 0.15))  # Отрисовываем поверхность кнопки
        sp_cord = [start_pos[0], start_pos[1], start_pos[0] + start_pos[2],
                   start_pos[1] + start_pos[3]]  # Получаем координаты поверхности кнопки

        rules_pos = screen.blit(text_rules, (screen_width / 2 - (rules_rect[2] / 2),
                                        screen_height / 2 - screen_height * 0.05))  # Отрисовываем поверхность кнопки
        rp_cord = [rules_pos[0], rules_pos[1], rules_pos[0] + rules_pos[2],
                   rules_pos[1] + rules_pos[3]]  # Получаем координаты поверхности кнопки

        quit_pos = screen.blit(text_quit, (screen_width / 2 - (quit_rect[2] / 2),
                                        screen_height / 2 + screen_height * 0.06))  # Отрисовываем поверхность кнопки
        qp_cord = [quit_pos[0], quit_pos[1], quit_pos[0] + quit_pos[2],
                   quit_pos[1] + quit_pos[3]]  # Получаем координаты поверхности кнопки

        for event in pygame.event.get():  # Выход
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:  # Отслеживаем нажатие пробела для закрытия окна правил
                if event.key == pygame.K_SPACE:
                    rules_wind = False  # Разблокируем кнопки меню
                    update = True  # Включаем обновление экрана

            # Отслеживаем положение курсора и ищем его на кнопке
            if event.type == pygame.MOUSEMOTION:
                if sp_cord[0] <= event.pos[0] <= sp_cord[2] and sp_cord[1] <= event.pos[1] <= sp_cord[3]:
                    selected = 'start'
                if rp_cord[0] <= event.pos[0] <= rp_cord[2] and rp_cord[1] <= event.pos[1] <= rp_cord[3]:
                    selected = 'rules'
                if qp_cord[0] <= event.pos[0] <= qp_cord[2] and qp_cord[1] <= event.pos[1] <= qp_cord[3]:
                    selected = 'quit'

            if event.type == pygame.MOUSEBUTTONDOWN and not rules_wind:
                if selected == "start":
                    game.start_game()  # Запуск игры
                if selected == "rules":  # Блок правил
                    screen.blit(bg_rules, (0, 0))  # Отображение заднего фона

                    # Вывод правил
                    text_rules1 = text_format('В начале игры шашки противоположных цветов (по 8 штук)', font, 21, black)
                    text_rules2 = text_format('расставляются на шахматной доске в крайних рядах напротив', font, 21,
                                              black)
                    text_rules3 = text_format('друг друга, после чего игроки по очереди пытаются щелчком', font, 21,
                                              black)
                    text_rules4 = text_format('выбить чужие шашки, при этом стараясь оставлять свои в игре.', font, 21,
                                              black)
                    text_rules5 = text_format('Игрок, выбивший все чужие шашки (и при этом на доске', font, 21,
                                              black)
                    text_rules6 = text_format('осталась хотя бы одна его шашка) побеждает в этом раунде.', font, 21,
                                              black)
                    text_rules7 = text_format('Нажмите пробел чтобы закрыть окно.', font, 28, black)

                    update = False  # Выключаем обновление экрана чтобы правила не исчезли сразу
                    rules_wind = True  # Блокируем кнопки меню

                    screen.blit(text_rules1, (screen_width / 2 - (text_rules1.get_rect()[2] / 2), 230))
                    screen.blit(text_rules2, (screen_width / 2 - (text_rules2.get_rect()[2] / 2), 260))
                    screen.blit(text_rules3, (screen_width / 2 - (text_rules3.get_rect()[2] / 2), 290))
                    screen.blit(text_rules4, (screen_width / 2 - (text_rules4.get_rect()[2] / 2), 320))
                    screen.blit(text_rules5, (screen_width / 2 - (text_rules5.get_rect()[2] / 2), 350))
                    screen.blit(text_rules6, (screen_width / 2 - (text_rules6.get_rect()[2] / 2), 380))
                    screen.blit(text_rules7, (screen_width / 2 - (text_rules7.get_rect()[2] / 2), 430))
                    #  Обновляем окно чтобы всё отобразилось
                    pygame.display.update()
                if selected == "quit":
                    pygame.quit()  # Выход из игры
                    quit()
        if update:
            pygame.display.update()
        pygame.display.set_caption("Чапаев")  # Название окна


main_menu()
pygame.quit()
quit()
