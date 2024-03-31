import pygame
import sys
from button_sprite import load_image

cell_size = 50
minor_grid_size = 1
major_grid_size = 3
buffer = 5
button_height = 50
button_width = 125
button_border = 2
width = cell_size*9 + minor_grid_size*6 + major_grid_size*4 + buffer*2
height = cell_size*9 + minor_grid_size*6 + \
    major_grid_size*4 + button_height + buffer*3 + button_border*2
size = width, height
white = 255, 255, 255

def terminate():
    pygame.quit()
    sys.exit()

def start_window(screen):
    FPS = 50
    intro_text = ["СУДОКУ", "",
                  "Правила игры", "",
                  "Три уровня сложности, можно сдаться",
                  "и перейти на следующий с помощью стрелки.",
                  "Кнопка solve покажет правильное решение.",
                  "Кнопка reset перезапустит текущий уровень.",
                  "Идет подсчет правильно решеных уровней."]

    fon = pygame.transform.scale(load_image('fon.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 28)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, white)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)

def end_window(screen, correct_levels):
    FPS = 50
    intro_text = ["КОНЕЦ ИГРЫ", "",
                  f"Правильно решено уровней: {correct_levels}"]

    if correct_levels < 3:
        fon = pygame.transform.scale(load_image('fon_bad_end.png'), size)
    else:
        fon = pygame.transform.scale(load_image('fon_good_end.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 28)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, white)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)