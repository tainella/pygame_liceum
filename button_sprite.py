import pygame
import os, sys

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, group, filename, pressed_filename, x, y, width, height):
        super().__init__(group)
        self.filename = filename
        self.pressed_filename = pressed_filename
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(load_image(filename), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_pressed = False

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = pygame.transform.scale(load_image(self.pressed_filename), 
                                                (self.width, self.height))
            self.is_pressed = True
        elif self.is_pressed:
            self.image = pygame.transform.scale(load_image(self.filename), 
                                                (self.width, self.height))
            self.is_pressed = False