#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

#music
mixer.init()
mixer.music.load("f7c571af32330a5.mp3")
mixer.music.play()
finish_sound = mixer.Sound("jg-032316-sfx-8-bit-bounce-sound.mp3")
kick_sound = mixer.Sound("jg-032316-sfx-8-bit-punch.mp3")
fire_sound = mixer.Sound("fire.ogg")

met_image = "asteroid.png"
img_enemy ="ufo.png"
img_bullet = "bullet.png"
img_kit = "pharmacy.png"

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 30)
win = font1.render("YOU WIN", True, (255, 255, 255))
lose = font1.render("YOU LOSE", True, (180, 0, 0))

lost = 0
score = 0
hp = 3

size_x_met = 50
size_y_met = 50

win_weight = 500
win_height = 900  

FPS = 60
speed = 10
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

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_weight - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)




class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_weight - 80)
            self.rect.y = randint(-50, 0)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_weight - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class First_aid_kit(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_weight - 80)
            self.rect.y = randint(-50, 0)


display.set_caption('star wars')
window = display.set_mode((win_weight, win_height))
background = transform.scale(image.load("v907-aum-08.jpg"), (win_weight, win_height))
background = transform.scale(image.load("galaxy.jpg"), (win_weight, win_height))

rocket = Player("svrsvr.png", 225, 750, 75, 125, 10)

monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy(img_enemy, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
    monsters.add(monster)
bullets = sprite.Group()

meteors = sprite.Group()
for i in range(1, 5):
    meteor = Meteor(met_image, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
    meteors.add(meteor)
player_gr = sprite.Group()
player_gr.add(rocket)

first_aid_kits = sprite.Group()
for i in range(1, 2):
    first_aid_kit = First_aid_kit(img_kit, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
    first_aid_kits.add(first_aid_kit)

num_fire = 0
max_lose = 5

finish = False
run = True
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:        
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False: 
                    num_fire = num_fire + 1
                    fire_sound.play()
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_r:
                finish = False
                score = 0
                lost = 0
                hp = 3
                num_fire = 0
                for b in bullets:
                    b.kill()
                for m in monsters:
                    m.kill()
                for k in first_aid_kits:
                    k.kill()
                for p in player_gr:
                    p.kill()
                for met in meteors:
                    met.kill()

                for i in range(1, 2):
                    first_aid_kit = First_aid_kit(img_kit, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
                    first_aid_kits.add(first_aid_kit)
                
                for i in range(1, 5):
                    meteor = Meteor(met_image, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
                    meteors.add(meteor)

                for i in range(1, 5):
                    monster = Enemy(img_enemy, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
                    monsters.add(monster)
                
                rocket = Player("svrsvr.png", 225, 750, 75, 125, 10)
                player_gr.add(rocket)

    if not finish:
        window.blit(background, (0, 0))

        rocket.update()
        bullets.update()
        meteors.update()
        monsters.update()
        first_aid_kits.update()
        monsters.draw(window)
        player_gr.draw(window)
        meteors.draw(window)
        bullets.draw(window)
        first_aid_kits.draw(window)
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font2.render("reload", 1, (150, 0, 0))
                window.blit(reload, (240, 460))
            else:
                num_fire = 0
                rel_time = False

        colides = sprite.groupcollide(monsters, bullets, True, True)
        colides1 = sprite.groupcollide(meteors, bullets, True, True)
        colides2= sprite.groupcollide(player_gr, meteors, False, True)
        colides3= sprite.groupcollide(player_gr, monsters, False, True)
        colides4 = sprite.groupcollide(player_gr, first_aid_kits, False, True)

        text_sc = font2.render("Счеи:" + str(score), 1, (255, 255, 255))
        window.blit(text_sc, (10, 20))

        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))   

        text_hp = font2.render("жизни:" + str(hp), 1, (255, 255, 255))
        window.blit(text_hp, (10, 80))

        for c in colides:
            score = score + 1
            monster = Enemy(img_enemy, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
            monsters.add(monster)

        for c in colides1:
            score = score + 1
            meteor = Meteor(met_image, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
            meteors.add(meteor)

        for c in colides2:
            meteor = Meteor(met_image, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
            meteors.add(meteor)
            hp = hp - 1

        for c in colides3:
            monster = Enemy(img_enemy, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
            monsters.add(monster)
            hp = hp - 1

        for c in colides4:
            first_aid_kit = First_aid_kit(img_kit, randint(0, win_weight - 80), -40, 80, 50, randint(1, 4))
            first_aid_kits.add(first_aid_kit)
            hp = 3


        if hp == 0:
            finish = True
            window.blit(lose, (200, 200))

        if lost > max_lose:
            finish = True
            window.blit(lose, (200, 200))

        display.update()
    clock.tick(60)