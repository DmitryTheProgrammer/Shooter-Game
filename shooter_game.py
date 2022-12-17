import pygame
pygame.init()
import random

pygame.mixer.music.load('space.ogg')
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play()

bullet_sound = pygame.mixer.Sound('fire.ogg')
size = 50
font = pygame.font.SysFont('Arial', size)
W = 15
H = 15
window = pygame.display.set_mode((W*size, H*size))
background = pygame.transform.scale(pygame.image.load('galaxy.jpg'), (W*size, H*size))
timer = pygame.time.Clock()
pygame.display.set_caption('Maze')
ufo = pygame.image.load('ufo.png')
ufo = pygame.transform.scale(ufo, (50, 40))
bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (size//3, size//3))
rocket = pygame.image.load('rocket.png')
rocket = pygame.transform.scale(rocket, (size, size))

class GameObject():
    def __init__(self, x, y, w, h, image):
        self.hitbox = pygame.Rect(x, y, w, h)
        self.hitbox.center = (x, y)
        self.image = image
        self.x = x
        self.y = y


bullet_list = []


class Bullet(GameObject):
    def move(self):
        self.hitbox.y -= 10
        if self.hitbox.y < 0:
            bullet_list.remove(self)


class Hero(GameObject):
    speed = 10
    money = 0
    fail = 0
    def movement(self):
        buttons = pygame.key.get_pressed()
        if buttons[pygame.K_a] == True:
            self.hitbox.x -= self.speed
        if buttons[pygame.K_d] == True:
            self.hitbox.x += self.speed
        if self.hitbox.x > size*(W-1):
            self.hitbox.x -= self.speed
        if self.hitbox.x < 0:
            self.hitbox.x += self.speed

    def shooting(self):
        bullet = Bullet(self.hitbox.centerx, self.hitbox.centery, size//3, size//3, bullet_image)
        bullet_list.append(bullet)

class Enemy(GameObject):
    def __init__(self, x, y, w, h, color, speed_x, speed_y):
        GameObject.__init__(self, x, y, w, h, color)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def patrol(self):
        self.hitbox.x += self.speed_x
        self.hitbox.y += self.speed_y
        if self.hitbox.y > size*(H-2):
            self.hitbox.y = self.y
            self.hitbox.x = random.randint(0, size*14)
            hero.fail += 1
        if hero.fail > 3:
            hero.fail = 0
            hero.money = 0
            hero.hitbox.x = hero.x
            for enemy in enemy_list:
                enemy.hitbox.x = random.randint(0, size*14)
                enemy.hitbox.x = enemy.y
            
    def collide(self):
        if self.hitbox.colliderect(hero.hitbox):
            hero.money = 0
            hero.fail = 0
            hero.hitbox.x = hero.x
            hero.hitbox.y = hero.y
            self.hitbox.x = random.randint(0, size*14)
            self.hitbox.y = self.y
        for bullet in bullet_list:
            if bullet.hitbox.colliderect(self.hitbox):
                self.hitbox.x = random.randint(0, size*14)
                self.hitbox.y = self.y
                bullet_list.remove(bullet)
                hero.money += 1
                break
box_list = []
enemy_list = []

def info():
    score_image = font.render('Счёт: ' + str(hero.money), True, (255, 255, 255))
    fail_image = font.render('Пропущено: ' + str(hero.fail), True, (255, 255, 255))
    window.blit(score_image, (0, 0))
    window.blit(fail_image, (0, size))   

hero = Hero(size*(W//2), size*(H-2), size, size, rocket)
for i in range (7):
    enemy_list.append(Enemy(random.randint(0, size*14), size*(-i), size, size, ufo, 0, 1))

while True:
    window.blit(background, (0, 0))
    events_list = pygame.event.get()
    for event in events_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_sound.play()
                hero.shooting()
    for box in box_list:
        window.blit(box.image, box.hitbox)
    hero.movement()
    info()
    window.blit(hero.image, hero.hitbox)
    for guardian in enemy_list:
        window.blit(guardian.image, guardian.hitbox)
        guardian.patrol()
        guardian.collide()
    for bullet in bullet_list:
        window.blit(bullet.image, bullet.hitbox)
        bullet.move()
    pygame.display.update()
    timer.tick(60)