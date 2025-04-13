import pygame
import random



WIDTH = 440
HEIGHT = 800
FPS = 60

WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
RED = pygame.Color('red')
GREEN = pygame.Color('green')
BLUE = pygame.Color('blue')
YELLOW = pygame.Color('yellow')
AQUA = pygame.Color((0, 255, 255))
PURPLE = pygame.Color('purple')
GREY = pygame.Color((85, 85, 85))

# Инициализация Pygame
pygame.init()
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('data/pew.mp3')
shoot_sound.set_volume(0.2)
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.set_volume(0.1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Road!")
clock = pygame.time.Clock()
color = ''

# Шрифт
font_name = pygame.font.match_font('arial')


# Функция для рисования текста
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Функция для создания машины-противника
def newmob():
    a = 0
    m = Mob()
    all_sprites.add(m)
    if a % 2 == 0:
        mobs.add(m)
    else:
        mobs2.add(m)


#  Функция для отображения уровня здоровья
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


# Фунция для начального экрана и экрана перезагрузки
def show_go_screen():
    img_start = pygame.image.load('data/starter_frame.png')
    img_start = pygame.transform.scale(img_start, (440, 800))
    rect = img_start.get_rect()
    screen.blit(img_start, rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False


# Функция выбора цвета машины
def show_сolor_of_car():
    img_color = pygame.image.load('data/choice_color.png')
    img_color = pygame.transform.scale(img_color, (440, 800))
    rect = img_color.get_rect()
    screen.blit(img_color, rect)
    pygame.draw.rect(screen, RED, (40, 120, 160, 160))
    pygame.draw.rect(screen, BLUE, (240, 120, 160, 160))
    pygame.draw.rect(screen, YELLOW, (40, 360, 160, 160))
    pygame.draw.rect(screen, PURPLE, (240, 360, 160, 160))
    pygame.draw.rect(screen, GREY, (120, 600, 200, 160))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        global color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 40 and pygame.mouse.get_pos()[1] >= 80:
                    if pygame.mouse.get_pos()[0] <= 200 and pygame.mouse.get_pos()[1] <= 240:
                        color = 'enemy.png'
                        waiting = False
                if pygame.mouse.get_pos()[0] >= 240 and pygame.mouse.get_pos()[1] >= 80:
                    if pygame.mouse.get_pos()[0] <= 400 and pygame.mouse.get_pos()[1] <= 240:
                        color = 'car-blue.png'
                        waiting = False
                if pygame.mouse.get_pos()[0] >= 40 and pygame.mouse.get_pos()[1] >= 320:
                    if pygame.mouse.get_pos()[0] <= 200 and pygame.mouse.get_pos()[1] <= 480:
                        if random.random() >= 0.5:
                            color = 'car-yellow.png'
                            waiting = False
                        else:
                            color = 'bus.png'
                            waiting = False
                if pygame.mouse.get_pos()[0] >= 240 and pygame.mouse.get_pos()[1] >= 320:
                    if pygame.mouse.get_pos()[0] <= 400 and pygame.mouse.get_pos()[1] <= 480:
                        color = 'car-player-purple.png'
                        waiting = False
                if pygame.mouse.get_pos()[0] >= 120 and pygame.mouse.get_pos()[1] >= 560:
                    if pygame.mouse.get_pos()[0] <= 320 and pygame.mouse.get_pos()[1] <= 720:
                        if random.random() >= 0.6:
                            color = 'Metr.png'
                        else:
                            color = 'Lorry.png'
                        waiting = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
                color = 'plane_1.png'
                waiting = False
            if keys[pygame.K_q] and keys[pygame.K_e]:
                color = 'BTR.png'
                waiting = False


# Спрайт игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'data/{color}')
        if color == 'plane_1.png':
            self.image = pygame.transform.scale(self.image, (100, 200))
        else:
            self.image = pygame.transform.scale(self.image, (75, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.health = 100
        self.count = False

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# Спрайт машин-противников
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = [35, 181, 337]
        self.colors = ['data/enemy.png', 'data/car-white.png', 'data/bus-top.png', 'data/enemy-purple.png', 'data/enemy-taxi.png', 'data/red_car.png', 'data/bus.png', 'data/Grey_car.png', 'data/Lorry.png']
        self.color = random.choice(self.colors)
        self.image = pygame.image.load(self.color)
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (75, 150))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(self.position)
        self.rect.y = -1000
        self.speedy = random.randrange(3, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.color = random.choice(self.colors)
            self.image = pygame.image.load(self.color)
            self.image = pygame.transform.rotate(self.image, 180)
            self.image = pygame.transform.scale(self.image, (75, 150))
            self.rect.x = random.choice(self.position)
            self.rect.y = -1000
            self.speedy = random.choice([10, 11, 14, 15])


# Класс взрывов при столкновениях
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Класс бонусов
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'shield'
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


# Запись графики в одну переменную
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(f'data/{filename}')
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (200, 200))
    explosion_anim['lg'].append(img_lg)

background = pygame.image.load('data/road.png')
background = pygame.transform.rotate(background, 90)
background = pygame.transform.scale(background, (440, 1000))
background_rect = background.get_rect()

powerup_images = {}
powerup_images['shield'] = pygame.image.load('data/shield_gold.png')
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Начало основного цикла
game_over = True
running = True
while running:
    # В начале появляется начальный экран
    if game_over:
        pygame.mixer.music.play()
        show_go_screen()
        show_сolor_of_car()
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Вызов графики
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        mobs = pygame.sprite.Group()
        mobs2 = pygame.sprite.Group()
        for i in range(2):
            newmob()
        score = 0
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()
    # Проверка на столкновение
    hits = pygame.sprite.spritecollide(player, mobs, True)
    for hit in hits:
        player.health -= 50
        newmob()
        # Вызов взрыва
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        shoot_sound.play()
        # При столкновении, с шансом 20% может из машины выпасть бонус восстанавливающий здоровье
        if random.random() > 0.8:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        # Если здоровье закончилось, то игра заканчивается
        if player.health <= 0:
            game_over = True
    # Проверка на столкновение игрока с бонусом
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        player.health += 100
        if player.health >= 100:
            player.health = 100
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # Счётчик очков игрока
    score += 1 / FPS
    draw_text(screen, str(int(score)), 30, WIDTH / 2, 10, WHITE)
    # Полоска хп
    draw_shield_bar(screen, 15, 15, player.health)
    pygame.display.flip()
pygame.quit()
