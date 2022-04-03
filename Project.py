from pygame import *
from random import randint
from time import time as timer
from time import sleep
import pickle
score_global = 0
win_width = 700
win_height = 500
max_lost = 12
max_win = 30
finish = False
speed_enemy_max = 3
hard = 0
speed_enemy_min = 1

#!
#TODO
print("Работает")
load_file = open("save.dat", "rb")
score_global = pickle.load(load_file)
load_file.close()
#mouse.set_visible(False)
MANUAL_CURSOR = image.load('asteroid.png')

img_back = "galaxy.jpg"
img_player = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_fonwin = "Fonwin.jpg"
img_fonlose = "fonlose.jpg"
img_asteroid = "asteroid.png"
life = 5
backgroudwin = transform.scale(
    image.load(img_fonwin), (win_width, win_height)
    )
backgroudlose = transform.scale(
    image.load(img_fonlose), (win_width, win_height)
    )
score = 0
lost = 0
anti_hard_1 = False
anti_hard_2 = False
window = display.set_mode(
    (win_width, win_height)
    )
display.set_caption("Air Shooter - GameMode - UFO BETA")
backgroud = transform.scale(
    image.load(img_back), (win_width, win_height)
    )
display.set_icon(image.load("ufo.png"))


def hard_system():
    global anti_hard_1
    global anti_hard_2
    global speed_enemy_max
    global speed_enemy_min
    if hard == 5 and anti_hard_1 == False:
        speed_enemy_max = speed_enemy_max + 1
        anti_hard_1 = True
    elif hard == 10 and anti_hard_2 == False:
        asteroid = Asteroid(img_asteroid, randint(30, win_width -30), -40, 80, 50, randint(1, 1))
        asteroids.add(asteroid)
        speed_enemy_max = speed_enemy_max + 1
        speed_enemy_min = speed_enemy_min + 1
        anti_hard_2 = True





mixer.init()
mixer.music.load("musiconbackground.mp3")
mixer.music.play()
#fire_sound = mixer.Sound("fire.ogg")
font.init()

#font2 = font.SysFont('helvetica', 36)
font2 = font.Font(None, 36)
font1 = font.Font(None, 80)
win = font1.render("Ты выиграл!", True, (250, 250, 250))
lose = font1.render("Ты проиграл!", True, (180, 0, 0))
game = True
FPS = 70
clock = time.Clock()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 340:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

ship = Player(img_player, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 3):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(speed_enemy_min, speed_enemy_max))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 2):
    asteroid = Asteroid(img_asteroid, randint(30, win_width -30), -40, 80, 50, randint(1, 1))
    asteroids.add(asteroid)
rel_time = False
num_fire = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()
            if num_fire >= 10 and rel_time == False:
                last_time = timer()
                rel_time = True
    if not finish:
        window.blit(backgroud, (0, 0))
        text = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущеные: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        record = font2.render("Рекорд: " + str(score_global), 1, (250, 250, 250))
        window.blit(record, (10, 80))
        if life >= 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0 ,0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 0.8:
                reload = font2.render("Перезаряда", 1, (150, 0, 0))
                window.blit(reload, (260, 460))


            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score = score + 1
            hard = hard + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(speed_enemy_min, speed_enemy_max))
            monsters.add(monster)


        if sprite.spritecollide(ship, monsters, False):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)
            sprite.spritecollide(ship, monsters, True)
            score = score + 1
            life = life - 1


        if sprite.spritecollide(ship, asteroids, False):
            asteroid = Asteroid(img_asteroid, randint(30, win_width -30), -40, 80, 50, randint(1, 2))
            asteroids.add(asteroid)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if score > score_global:
            score_global = score
            save_file = open("save.dat", "wb")
            pickle.dump(score_global, save_file)
            save_file.close()


        if life == 0 or lost >= max_lost:

            finish = True
            window.blit(backgroudlose, (0, 0))
            window.blit(lose, (200, 200))

        if score>= max_win:

            finish = True
            window.blit(backgroudwin, (0, 0))
            window.blit(win, (200, 200))
        hard_system()
        


        display.update()
    window.blit(MANUAL_CURSOR, (mouse.get_pos()))
    clock.tick(FPS)
