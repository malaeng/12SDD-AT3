import pygame
from laser import Laser
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, constraint: int):
        super().__init__()
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 8
        self.damage = 20
        self.health = 500
        self.max_health = self.health
        self.max_x_constraint = constraint

        self.charged = True
        self.time_shot = 0
        self.cooldown = 150

        self.lasers = pygame.sprite.Group()



        # Audio
        self.laser_SFX_01 = pygame.mixer.Sound('audio/laserSmall_001.ogg')
        self.laser_SFX_02 = pygame.mixer.Sound('audio/laserSmall_002.ogg')
        self.laser_SFX_03 = pygame.mixer.Sound('audio/laserSmall_003.ogg')
        self.laser_SFX_04 = pygame.mixer.Sound('audio/laserSmall_004.ogg')

        self.laser_SFX_02.set_volume(0.3)

    def get_input(self):
        # Instead of checking for key_down and key_up as in the tutorial, stores all keys as a true or false value, for if they are being pressed or not.
        # To react to input, a pre-test loop checks if the value of a certain key is true - if it is being pressed
        keys = pygame.key.get_pressed()


        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = pygame.image.load('graphics/player_right.png').convert_alpha()
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = pygame.image.load('graphics/player_left.png').convert_alpha()
        else:
            self.image = pygame.image.load('graphics/player.png').convert_alpha()

        if keys[pygame.K_SPACE] and self.charged:
            self.shoot()
            self.charged = False
            self.time_shot = pygame.time.get_ticks()

    def shoot(self):
        pygame.mixer.Sound.play(self.laser_SFX_02)
        self.lasers.add(Laser(self.rect.center, (0, -16), self.rect.bottom))

    def recharge(self):
        if not self.charged:
            current_time = pygame.time.get_ticks()
            if current_time - self.time_shot >= self.cooldown:
                self.charged = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def take_damage(self, damage):
        self.health -= damage
        self.image.set_alpha(200)
        if self.health <= 0: 
            pass

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
        
class Healthbar(pygame.Surface):
    def __init__(self, pos:tuple, size: tuple, percent: float):
        super().__init__(size)
        self.width = size[0]
        self.height = size[1]
        self.health_percent = percent
        self.colours = {
            'border': '#fbf5ef',
            'hi_health': '#8b6d9c',
            'lo_health': '#c69fa5'
        }
        self.pos = pos

        self.fill(self.colours['border'])
        #self.update(self.health_percent)
        #self.percent_image = pygame.Surface((self.width*percent-8, self.height-8))
        #self.percent_image.fill((random.choice(('red', 'blue'))))
        

    def process(self, percent: float):
        if percent >= 0 :
            self.percent_image = pygame.Surface((self.width-8, self.height-8))
            self.percent_image = pygame.transform.scale_by(self.percent_image, (percent, 1))
            self.percent_image.fill(self.colours['hi_health' if percent > 0.3 else 'lo_health'])
            self.percent_image_rect = self.percent_image.get_rect(topleft = (4, 4))

            self.fill(self.colours['border'])
            self.blit(self.percent_image, self.percent_image_rect)











