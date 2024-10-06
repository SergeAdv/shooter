#Создай собственный Шутер!

from pygame import *
from random import randint, shuffle
from time import time as timer

font.init()
font2 = font.SysFont('Arial', 30)
lose = font2.render('YOU LOSE!',True,(255,0,0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.player_image = player_image
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale(image.load(player_image), (self.size_x, self.size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < window_width - 80:
            self.rect.x += self.speed
    def fire(self):
        i = randint(0,4)
        bullet = Bullet(bullets1[i], self.rect.centerx, self.rect.top, -15, 50, 90)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > window_height:
            self.rect.x = randint(80, window_width - 120)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
clock = time.Clock()
window = display.set_mode((1000, 800))
display.set_caption('Лабиринт')
window_width = 1000
window_height = 800
background = transform.scale(image.load("minions.jpg"),(1000,800))
lose = transform.scale(image.load("gafgaf.jpg"),(1000,800))
win = transform.scale(image.load("winwin.jpg"),(1000,800))
hero = Player('hero.png', 500, 650, 10, 150, 150)
bullets = set()
bullets1 = ['banana.png', 'banana.png','banana.png','banana.png','bananafu.png']

monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy('villian.png', randint(80, window_width - 120), -40, randint(1,2), 150, 150)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('mandarin.png', randint(80, window_width - 80), -40, randint(1,2),80, 50)
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('mainsound.mp3')
mixer.music.play()
mixer.music.set_volume(0.1)
lost = 0 #пропущенно кораблей
score = 0
goal = 20
max_lost = 10
life = 3
num_fire = 0 
rel_time = False
firesound = mixer.Sound('smeh_minonov.ogg')
finish = False
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire+=1
                    firesound.play()
                    hero.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Счёт: " + str(score), 1, (0,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (0,255,255))
        window.blit(text_lose, (10,50))
        hero.reset()
        hero.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        for b in bullets:
            b.update()
            b.reset()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 2, (200,0,0))
                window.blit(reload, (10,750))
            else:
                num_fire = 0
                rel_time = False
        for b in bullets:
            if sprite.spritecollide(b, monsters, False):
                if not(b.player_image == 'bananafu.png'):
                    sprite.spritecollide(b,monsters, True)
                    b.size_x = 0
                    b.size_y = 0
                    b.image = transform.scale(image.load(b.player_image), (b.size_x, b.size_y))
                    b.rect = b.image.get_rect()
                    monster = Enemy('villian.png', randint(80, window_width - 80), -40, randint(1, 5), 150, 150)
                    monsters.add(monster) 
                    score+=1
        
        if lost >= max_lost or life == 0:
            finish = True
            window.blit(lose, (0,0))
        if score > goal:
            finish = True
            window.blit(win, (0,0))
        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, asteroids, False):
            sprite.spritecollide(hero, monsters, True)
            sprite.spritecollide(hero, asteroids, True)
            life-=1
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        text_life = font2.render('Осталось жизней: '+str(life), 50, life_color)
        window.blit(text_life, (650,10))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        bullets.clear()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()   
        
        time.delay(3000)
        for i in range(1, 5):
            monster = Enemy('villian.png', randint(80, window_width - 80), -40, randint(1, 5), 150, 150)
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy('mandarin.png', randint(30, window_width - 30), -40, randint(1, 7), 80, 50)
            asteroids.add(asteroid)   


    time.delay(10)


