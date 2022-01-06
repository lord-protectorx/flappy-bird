import os
import pygame

pygame.init()

size = width, height = 600, 600
screen = pygame.display.set_mode(size)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
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


class Bird(pygame.sprite.Sprite):
    image = load_image("bird.png", -1)
    gravity = 0.5

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Bird.image
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = 283
        self.rect.y = 288
        self.speed = 0

    def update(self):
        self.speed += Bird.gravity
        self.rect = self.rect.move(0, self.speed)

    def jump(self):
        self.speed = -13


all_sprites = pygame.sprite.Group()

bird = Bird()

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            Bird.jump(bird)
    screen.fill(pygame.Color("red"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
