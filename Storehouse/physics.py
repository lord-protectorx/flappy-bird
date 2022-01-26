import pygame
import sys
import os
import random

FPS = 50

pygame.init()

size = width, height = 600, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('../data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Best score']

    fon = pygame.transform.scale(load_image('menu.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/Flappy-Bird.ttf', 40)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 230
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

start_screen()


def draw_platform():
    screen.blit(plat_age, (pos_x, 546))
    screen.blit(plat_age, (pos_x + 336, 546))


back_age1 = pygame.transform.chop(load_image("background_win.png"), (0, 300, 300, 0))
back_age2 = pygame.transform.scale(back_age1, (600, 600))
plat_age = pygame.transform.scale(load_image("base.png"), (336, 56))
pos_x = 0
pipe_per = 150
speed = 2
pipe_range = 1500
last_pipe = pygame.time.get_ticks() - pipe_range


class Bird(pygame.sprite.Sprite):
    image = load_image("bird.png", -1)
    gravity = 0.6
    flag = True

    def __init__(self):
        super().__init__(bird_group)
        self.image = Bird.image
        self.rect = self.image.get_rect()
        # создаем маски

        self.rect.x = 283
        self.rect.y = 288
        self.speed = 0

    def update(self):
        if not pygame.sprite.collide_mask(self, btm_pipe) and not pygame.sprite.collide_mask(self, top_pipe) and self.flag:
            self.speed += Bird.gravity
            self.rect = self.rect.move(0, self.speed)
        if self.rect.y > 530 or self.rect.y < 5:
            self.flag = False

    def jump(self):
        self.speed = -8


class Pipe(pygame.sprite.Sprite):
    def __init__(self, posis, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale2x(load_image("pipe_up.png"))
        self.rect = self.image.get_rect()
        # создаем маску
        self.mask = pygame.mask.from_surface(self.image)

        if posis == 1:  # top
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x_pos, y_pos - int(pipe_per / 2)]
        if posis == -1:  # bottom
            self.rect.topleft = [x_pos, y_pos + int(pipe_per / 2)]

    def update(self):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()


f1 = pygame.font.Font('data/Flappy-Bird.ttf', 50)
bird_group = pygame.sprite.Group()
bird = Bird()
count = 0
pipe_group = pygame.sprite.Group()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            Bird.jump(bird)

    screen.blit(back_age2, (0, 0))
    pos_x -= speed

    pipe_group.update()
    pipe_group.draw(screen)
    Now_time = pygame.time.get_ticks()
    if Now_time - last_pipe > pipe_range:
        pipe_heig = random.randint(-100, 100)
        y_pos = 300 + pipe_heig
        x_pos = 600
        btm_pipe = Pipe(-1, pipe_group)
        top_pipe = Pipe(1, pipe_group)
        last_pipe = Now_time
        count += 1

    draw_platform()
    if pos_x <= -72:
        pos_x = 0

    bird_group.draw(screen)
    bird_group.update()
    if not bird.flag:
        running = False
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        running = False
    if count - 2 >= 0:
        text1 = f1.render(f'{count - 2}', True, (255, 255, 255))
        screen.blit(text1, (300, 50))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
print('')
