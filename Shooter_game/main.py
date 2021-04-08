import pygame as pg
import random as r
import math
from os import *


# Game object classes
####################################################################

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.sheild = 100
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH / 2)
        self.rect.bottom = (HEIGHT - (HEIGHT * .05))
        self.speedx = 0
        # self.shoot_delay
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hide_timer = pg.time.get_ticks()
        self.hidden = False
        self.power_level = 1
        self.powTimer = pg.time.get_ticks()

    def hide(self):
        # hide the player temporarily
        self.lives -= 1
        self.hiden = True
        self.hide_time = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        self.sheild = 100

    def update(self):
        # unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 3000:
            self.hidden = False
            self.rect.bottom(HEIGHT - (HEIGHT * .05))
            self.rect.centerx = (SIDTH / 2)

    def gun_pow_up(self):
        self.power_level += 1
        self.powTimer = pg.time.get_ticks()

    def sheilds_up(self, num):
        player.sheild += r.randint(15, 50)
        if player.sheild >= 100:
            player.sheild = 100

    def update(self):
        # time out power ups
        if self.power_level >= 2 and pg.time.get_ticks() - self.powTimer > POWERUP_TIME:
            self.power_level -= 1
            self.powTimer = pg.time.get_ticks()

        # basic movement side to side
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.speedx = 5
        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.speedx = -5
        # if keystate[pg.K_SPACE]:
        #     self.shoot()

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

        self.rect.x += self.speedx

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power_level == 1:
                b = Bullet(self.rect.centerx, self.rect.top + 1)
                all_sprites.add(b)
                bullet_group.add(b)
                shoot_snd.play()

            elif self.power_level >= 2:
                b1 = Bullet(self.rect.left, self.rect.centery)
                b2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(b1)
                bullet_group.add(b1)
                all_sprites.add(b2)
                bullet_group.add(b2)
                shoot_snd.play()

            elif self.power_level >= 3:
                b = Bullet(self.rect.centerx, self.rect.top + 1)
                b1 = Bullet(self.rect.left, self.rect.centery)
                b1.inc_spred(-3)
                b2 = Bullet(self.rect.right, self.rect.centery)
                b.inc_spred(3)
                all_sprites.add(b1)
                bullet_group.add(b1)
                all_sprites.add(b2)
                bullet_group.add(b2)
                all_sprites.add(b)
                bullet_group.add(b)
                shoot_snd.play()


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        # self.image = pg.Surface((5, 10))
        # self.image.fill(BLUE)
        self.image = bullet_img
        self.image = pg.transform.scale(self.image, (15, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10
        self.spread = 0

    def inc_spred(self, num):
        self.spread = num

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.spread
        # kill the bullet when bottom < screen
        if self.rect.bottom < 0:
            self.kill()


class Star(pg.sprite.Sprite):
    pass


class NPC(pg.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()
        self.image = pg.Surface((25, 25))
        self.image.fill(RED)
        ##self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # self.rect.centerx = (WIDTH / 2)
        # self.rect.top = (0)
        # self.speed = -10
        self.rect.x = r.randrange(WIDTH - self.rect.width)
        self.rect.y = r.randrange(-100, -40)
        self.speedy = r.randrange(1, 8)
        self.rot = 0  # rotation
        self.rot_speed = r.randint(-8, 8)
        self.update = pg.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = r.randrange(WIDTH - self.rect.width)
            self.rect.y = r.randrange(-100, -40)
            self.speedy = r.randrange(1, 8)


    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 60:
            self.last_update = now
            # do the rotation
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_oirig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx



class Explostion(pg.sprite.Sprite):
    def __init__(self, center, size):
        super(Explostion, self).__init__()
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size])
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        super(Pow, self).__init__()
        self.type = r.choice(powerUps_chance)
        self.image = pows_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


####################################################################


# Game Constants
####################################################################
HEIGHT = 900
WIDTH = 600
FPS = 60

# Colors (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

title = "Shmup"
font_name = pg.font.match_font("arial")

powerUps_list = ["gun", "sheild"]
powerUps_chance = ["gun", "gun", "sheild", "sheild", "sheild", "sheild", "sheild", "sheild", "sheild", "sheild",
                   "sheild"]

POWERUP_TIME = 10000

font_name = pg.font.match_font("arial")
####################################################################

# initialize pygame and create window
####################################################################
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()
####################################################################
# folder variables
####################################################################
game_folder = path.dirname(__file__)
imgs_folder =  path.join(game_folder, 'imgs')
snd_folder = path.join(game_folder, 'snds')
scores_folder = path.join(game_folder, 'scores')
background_folder = path.join(imgs_folder, 'backgrounds')
enemy_imgs_folder = path.join(imgs_folder, 'enemy_imgs')
player_imgs_folder = path.join(imgs_folder, 'player_imgs')


pow_folder = path.join(imgs_folder, "pows")

#####################################################################


# load imgs
####################################################################
# load imgs
####################################################################
#back grond img loaded
background = pg.image.load(path.join(background_img_folder,"starfield.png")).convert()
background = pg.transform.scale(background,(WIDTH,HEIGHT))
background_rect = background.get_rect()
#player img loaded
player_img = pg.image.load(path.join(player_img_folder,"player1Ship.png")).convert()
npc_img = pg.image.load(path.join(enemy_img_folder,"img_1.png")).convert()
bullet_img = pg.image.load(path.join(player_img_folder,"bullet_img.png")).convert()
explosion_anim = {}
explosion_anim["lg"] =[]
explosion_anim["sm"] = []
expostion_anim["player"] = []
meteor_images = []#insert (copy, paste)asteroid into list
player_mini_img = pg.transform.acale(player_img,(25,19))
player_mini_img.set_colorkey(BLACK)
for img in meteor_images.append(pg.image.load(path.join(enemy_img_folder, img)))

    for i in range(9):
        fn = "regularExplosion00.png".format(i)
        img = pg.image.load(path.join(npc_explosion_animate, fn)).convert()
        img_lg = pg.transform.scale(img, 100, 100)
        img_sm = pg.transform.scale(img, 40, 40)
        explosion_anim["sm"].append(img_sm)
        explosion_anim["lg"].append(img_lg)
        # adding player explosion
        fn = "sonicExplosion{}.png".format(i)
        img = pg.image.load(path.join(player_Player_expl, fn)).convert()
        img.set_colorkey(BLACK)
        explosion_anim["player"].append(img)

####################################################################

# create Sprite groups
####################################################################
all_sprites = pg.sprite.Group()
players_group = pg.sprite.Group()
npc_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
star_group = pg.sprite.Group()
pows_group = pg.sprite.Group()
###################################################################

# Game Loop
###################
# game update Variables
########################################
playing = True
game_over = True
score = 0
r.choice(expl_sounds).play()

########################################
################################################################
while playing:
    if game_over:
        show_go_screen()
        game_over = False
    # create Game Objects
    ###################################################################
    for i in range(25):
        star = Star()
        star_group.add(star)

    player = Player()

    npc = NPC()
    for i in range(10):
        npc = NPC()
        npc_group.add(npc)
    # bullet = Bullet(HEIGHT,WIDTH/2)
    ####################################################################

    # add objects to sprite groups
    ####################################################################
    players_group.add(player)
    # bullet_group.add(Bullet)
    npc_group.add(npc)

    for i in players_group:
        all_sprites.add(i)

    for i in npc_group:
        all_sprites.add(i)
    ####################################################################
    # timing
    ##################################################
    clock.tick(FPS)
    ##################################################

    # collecting Input
    ##################################################

    # Quiting the game when we hit the x
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
            if event.key == pg.K_ESCAPE:
                playing = False
        if event.type == pg.QUIT:
            playing = False

    ##################################################
    # Updates
    ##################################################
    all_sprites.update()

    # if NPC hits player
    hits = pg.sprite.spritecollide(player, npc_group, False)
    if hits:
        if player.lives < = 0:
            game_over = False
        # npc.spawn()
    # if bullet hits npc
    hits = pg.sprite.groupcollide(npc_group, bullet_group, True, True)
    for hit in hits:
        score += 50 - hit.radius
        exlp = Explostion(hit.rect.center, "lg")
        all_sprites.add(exlp)
        npc.spawn()
        r.choice(expl_sounds).play()
        if r.random() > .85:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            pows_group.add(pow)

    hits = pg.sprite.spritecollide(player, pows_group, True, pg.sprite.collide_circle)
    for hit in hits:
        if hit.type == "sheild":
            num = r.random()
            player.sheilds_up(num)
        elif hit.type == "gun":
            player.gun_pow_up()

            ## expl = Explosion(hit.rect.center, "sm")
            ## all_sprites.add(expl)
            ## if player.sheild <= 0:
            ##     death_expl = Explosion(player.rect.center, "player")
            ##     all_sprites.add(death_expl)
            ##     player.hide()
            #2
            #3     if player.lives <= 0 and not death_expl.alive():
            #4         playing = False

    ## for hit in hits
    ##     score += 50 - hit.radius
    ## npc.spawn()

    ##################################################
    # Render
    ##################################################
    screen.fill(BLACK)
    screen.blit(background, background_rect)

    all_sprites.draw(screen)

    pg.display.flip()
    draw_text(screen, "Score: " + str(score), 18, WIDTH / 2, 10, WHITE)

    screen.fill(BLACK)
    all_sprites.draw(screen)

    pg.display.flip()
    ##################################################

pg.quit()
################################################################
#####################