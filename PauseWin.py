import os
import pygame
import sys

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


size = width, height = 256, 256
screen = pygame.display.set_mode(size)
screen.blit(load_image("background.png"), (0, 0))
all_sprites = pygame.sprite.Group()


class Home(pygame.sprite.Sprite):
    image = load_image("home_button.png")
    image2 = pygame.transform.scale(image, (80, 80))
    flag = False

    def __init__(self, group):
        super().__init__(group)
        self.image = Home.image2
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 30

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            Home.flag = True
            print('home')


class Reset(pygame.sprite.Sprite):
    image = load_image("reset_button.png")
    image2 = pygame.transform.scale(image, (70, 70))
    flag = False

    def __init__(self, group):
        super().__init__(group)
        self.image = Reset.image2
        self.rect = self.image.get_rect()
        self.rect.x = 140
        self.rect.y = 35

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            Reset.flag = True
            print('Reset')


class Continue(pygame.sprite.Sprite):
    image = load_image("next-button.png")
    image2 = pygame.transform.scale(image, (80, 80))
    flag = False

    def __init__(self, group):
        super().__init__(group)
        self.image = Continue.image2
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = 120

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            Continue.flag = True
            print('continue')


clock = pygame.time.Clock()
running = True
Home(all_sprites)
Reset(all_sprites)
Continue(all_sprites)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()