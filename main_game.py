import pygame
import sys
import os
import random

FPS = 50

pygame.init()


size = width, height = 600, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
f1 = pygame.font.Font('data/Flappy-Bird.ttf', 50)
btn_size = 205



def save_res(score):
    files = os.listdir("./data")
    if 'best_score.txt' in files:
        file = open('./data/best_score.txt', 'r', encoding="utf-8")
        best_score = file.read()
        if score > int(best_score):
            best_score = str(score)
        file.close()
        file = open('./data/best_score.txt', 'w', encoding="utf-8")
        file.write(str(best_score))
        file.close()
    else:
        file = open('./data/best_score.txt', 'w', encoding="utf-8")
        file.write(str(score))
        file.close()


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_image_bird(name, color_key=None):
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


def terminate():
    pygame.quit()
    sys.exit()


class Retry(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("button.png"), (205, 85))
    flag = False

    def __init__(self, group):
        super().__init__(group)
        self.image = Retry.image
        self.rect = self.image.get_rect()
        self.rect.x = (width / 2) - 205 / 2
        self.rect.y = 400

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.flag = True


def gameover_screen(score):
    button_sprites = pygame.sprite.Group()
    intro_text = [f'Score: {score}']
    retry = Retry(button_sprites)
    fon = pygame.transform.scale(load_image('background_over.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/Flappy-Bird.ttf', 40)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 230
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    save_res(score)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif retry.flag:
                start_screen()  # начинаем игру
            button_sprites.update(event)
        button_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    global all_sprites, bird_group, pipe_group, count

    count = 0
    all_sprites = pygame.sprite.Group()
    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image('menu.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/Flappy-Bird.ttf', 40)
    text_coord = 250

    files = os.listdir("./data")
    if 'best_score.txt' in files:
        file = open('./data/best_score.txt', 'r', encoding="utf-8")
        best_score = file.read()
        best_score = str(best_score)
        file.close()

        intro_text = [f'Best score: {best_score}']

        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 205
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                choose_win()  # выбираем сложность
        pygame.display.flip()
        clock.tick(FPS)


class Hard(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("hard_button.png"), (205, 85))
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
            self.flag = True


class Easy(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("easy_button.png"), (205, 85))
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
            self.flag = True


def choose_win():
    global easy, hard
    background1 = pygame.transform.chop(load_image("background_win.png"), (0, 300, 300, 0))
    background2 = pygame.transform.scale(background1, (600, 600))
    hard = Hard(all_sprites)
    easy = Easy(all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif easy.flag or hard.flag:
                main_game()
            all_sprites.update(event)
        screen.blit(background2, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)


def draw_platform():
    screen.blit(plat_age, (pos_x, 546))
    screen.blit(plat_age, (pos_x + 336, 546))


back_age1 = pygame.transform.chop(load_image("background_win.png"), (0, 300, 300, 0))
back_age2 = pygame.transform.scale(back_age1, (600, 600))
plat_age = pygame.transform.scale(load_image("base.png"), (336, 56))
pos_x = 0
pipe_per = 150


class Bird(pygame.sprite.Sprite):
    image = load_image_bird("bird.png", -1)
    gravity = 0.6
    flag = True
    sheet = load_image_bird("birds.png", -1)
    columns = 3
    rows = 1
    counter = int()

    def __init__(self):
        super().__init__(bird_group)
        self.rect = self.image.get_rect()
        self.frames = []
        self.cut_sheet(self.sheet, self.columns, self.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 283
        self.rect.y = 288
        self.speed = 0

    def update(self):
        if self.counter % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.counter += 1
        if self.flag:
            self.speed += Bird.gravity
            self.rect = self.rect.move(0, self.speed)
        if self.rect.y > 530 or self.rect.y < 5:
            self.flag = False

    def jump(self):
        if Hard.flag and not Easy.flag:
            self.speed = -9
        else:
            self.speed = -11

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))


class Pipe(pygame.sprite.Sprite):
    def __init__(self, posis, x, y, speed, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale2x(load_image("pipe_up.png"))
        self.rect = self.image.get_rect()
        # создаем маску
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed

        if posis == 1:  # top
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_per / 2)]
        if posis == -1:  # bottom
            self.rect.topleft = [x, y + int(pipe_per / 2)]

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


def main_game():
    global count, pos_x, last_pipe
    bird = Bird()
    running = True
    if hard.flag and not easy.flag:
        speed = 6
        pipe_range = 800
    else:
        speed = 3
        pipe_range = 1300
    last_pipe = pygame.time.get_ticks() - pipe_range
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()

        screen.blit(back_age2, (0, 0))
        pos_x -= speed

        pipe_group.update()
        pipe_group.draw(screen)
        now_time = pygame.time.get_ticks()
        if now_time - last_pipe > pipe_range:
            pipe_heig = random.randint(-90, 90)
            y_pos = 300 + pipe_heig
            x_pos = 600
            pipe_1 = Pipe(-1, x_pos, y_pos, speed, pipe_group)
            pipe_2 = Pipe(1, x_pos, y_pos, speed, pipe_group)
            last_pipe = now_time
            count += 1

        draw_platform()
        if pos_x <= -72:
            pos_x = 0

        score = count - 1
        bird_group.draw(screen)
        bird_group.update()
        if not bird.flag:
            gameover_screen(score)
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):

            gameover_screen(score)
        if score >= 0:
            text1 = f1.render(f'{score}', True, (255, 255, 255))
            screen.blit(text1, (300, 50))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
# истсинный игровой цикл


start_screen()
