import os
import pygame
import sys

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('../data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname).convert_alpha()
    return image


size = width, height = 600, 600
btn_size = 205
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


class Hard(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("home_button.png"), (205, 85))
    flag = False

    def __init__(self, group):
        super().__init__(group)
        self.image = Hard.image
        self.rect = self.image.get_rect()
        self.rect.x = (width / 2) - btn_size / 2
        self.rect.y = 200

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            Hard.flag = True
            print('easy')


class Easy(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("reset_button.png"), (205, 85))
    flag = False

    def __init__(self, group):
        super().__init__(group)
        self.image = Easy.image
        self.rect = self.image.get_rect()
        self.rect.x = (width / 2) - btn_size / 2
        self.rect.y = 300

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            Easy.flag = True
            print('hard')


def choose_win():
    back_age1 = pygame.transform.chop(load_image("background_win.png"), (0, 300, 300, 0))
    back_age2 = pygame.transform.scale(back_age1, (600, 600))
    clock = pygame.time.Clock()
    running = True
    Hard(all_sprites)
    Easy(all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif Easy.flag or Hard.flag:
                return
            all_sprites.update(event)
        screen.blit(back_age2, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)