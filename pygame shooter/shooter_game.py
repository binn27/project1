from pygame import *
from random import *
from time import sleep
window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    #Mendefinisikan sifat
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 

class Player(GameSprite):
   # metode untuk mengendalikan sprite dengan panah keyboard
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] == True:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] == True:
            self.rect.x += self.speed
        elif keys[K_SPACE] == True:
            self.fire()
    def fire(self):
        mixer.music.load('fire.ogg')
        mixer.music.play()
        bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 5)
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def update(self):
        #Caranya membuat turun terus menerus
        self.rect.y += self.speed
        if self.rect.y > 500: #Apakah y sudah berada di paling bawah
            global missed
            missed += 1
            self.rect.y = 0
            

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


missed = 0
enemy1 = Enemy('ufo.png', randint(100, 500), 50, 1)
enemy2 = Enemy('ufo.png', randint(100, 500), 50, 1)
enemy3 = Enemy('ufo.png', randint(100, 500), 50, 1)
enemy4 = Enemy('ufo.png', randint(100, 500), 50, 1)

bullet = Bullet('bullet.png', 350, 400, 4)
#Bikin grup & Tambahkan monster kedalam group
monsters = sprite.Group()
monsters.add(enemy1, enemy2, enemy3, enemy4)
bullets = sprite.Group()
bullets.add(bullet)
spaceship = Player('rocket.png', 350, 400, 4)
font.init()
font1 = font.Font(None, 36)
font3 = font.Font(None, 36)
poin = 0
font2 = font.Font(None, 80)
win = font2.render('YOU WIN', 1, (200, 200, 200))
lose = font2.render('YOU LOSE', 1, (200, 90, 90))
run = True
while run:
    window.blit(background, (0,0))
    texts = font1.render('Missed:   ' + str(missed), 1, (200, 90, 90))
    window.blit(texts, (200, 200))
    sprite_collide = sprite.spritecollide(spaceship, monsters, False)
    group_collide = sprite.groupcollide(monsters, bullets, True, True)
    for monster in group_collide:
        monster = Enemy('ufo.png', randint(100, 500), 50, 1)
        monsters.add(monster)
        poin += 1
    points = font3.render('Points:   ' + str(poin), 1, (200, 80, 90))
    window.blit(points, (100, 100))
    if poin == 20:
        window.blit(win, (250,250))
        display.update()
        sleep(3)
        run = False
    if sprite.spritecollide(spaceship, monsters, False):
        window.blit(lose, (250,250))
        display.update()
        mixer.music.load('allien.mp3')
        mixer.music.play()
        sleep(7)
        run = False
    if missed == 3:
        window.blit(lose, (250,250))
        display.update()
        mixer.music.load('allien.mp3')
        mixer.music.play()
        sleep(7)
        run = False
    spaceship.update()
    spaceship.reset()
    bullets.draw(window)
    bullets.update()
    monsters.draw(window)
    monsters.update()
    for e in event.get():
        if e.type == QUIT:
            run = False
    display.update()