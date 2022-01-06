import os
import pygame
import sys
import random

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_platform():
    screen.blit(plat_age, (pos_x, 546))
    screen.blit(plat_age, (pos_x + 336, 546))


size = width, height = 600, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

back_age1 = pygame.transform.chop(load_image("background_win.png"), (0, 300, 300, 0))
back_age2 = pygame.transform.scale(back_age1, (600, 600))
plat_age = pygame.transform.scale(load_image("base.png"), (336, 56))
pos_x = 0
pipe_per = 150
speed = 2
pipe_range = 1500
last_pipe = pygame.time.get_ticks() - pipe_range


class Pipe(pygame.sprite.Sprite):
    def __init__(self, posis, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale2x(load_image("pipe_up.png"))
        self.rect = self.image.get_rect()
        if posis == 1:  # top
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x_pos, y_pos - int(pipe_per / 2)]
        if posis == -1:  # bottom
            self.rect.topleft = [x_pos, y_pos + int(pipe_per / 2)]

    def update(self):
        self.rect.x -= speed


pipe_group = pygame.sprite.Group()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    draw_platform()
    if pos_x <= -72:
        pos_x = 0
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

