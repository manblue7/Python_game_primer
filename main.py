import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('jet_fighter.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(20, SCREEN_WIDTH - 400),
                random.randint(20, SCREEN_HEIGHT - 20),
            )
        )
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
                move_up_sound.play()
        if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
                move_down_sound.play()
        if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('missile.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load('cloud.png').convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect (
            center = (
                random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(1, 2)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < -20:
            self.kill()


pygame.mixer.init()
pygame.init()

pygame.mixer.music.load('Apoxode_-_Electric_1.wav')
pygame.mixer.music.play(loops=-1)

move_up_sound = pygame.mixer.Sound('Rising_putter.wav')
move_down_sound = pygame.mixer.Sound('Falling_putter.wav')
collision_sound = pygame.mixer.Sound('Collision.wav')

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 300)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 700)

ENDGAME = pygame.USEREVENT + 3
END_COLLISON_SOUND = pygame.USEREVENT + 4

player1 = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
        if event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        if event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        if event.type == END_COLLISON_SOUND:
            collision_sound.stop()
        if event.type == ENDGAME:
            running = False

    pressed_keys = pygame.key.get_pressed()
    clouds.update()
    player1.update(pressed_keys)
    enemies.update()
    

    screen.fill([130, 206, 230])

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    if pygame.sprite.spritecollideany(player1, enemies):
        move_down_sound.stop()
        move_up_sound.stop()
        collision_sound.play()
        player1.kill()
        pygame.time.set_timer(ENDGAME, 500000)
        pygame.time.set_timer(END_COLLISON_SOUND, 700)
        

    pygame.display.flip()

    clock.tick(240)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
