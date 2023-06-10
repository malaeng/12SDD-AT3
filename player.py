import pygame
from laser import Laser
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, constraint: int):
        super().__init__()
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 8
        self.damage = 30
        self.health = 600
        self.max_health = self.health
        self.max_x_constraint = constraint

        self.charged = True
        self.time_shot = 0
        self.cooldown = 150

        self.lasers = pygame.sprite.Group()



        # Audio
        self.laser_SFX = pygame.mixer.Sound('audio/laserSmall_002.ogg')
        self.laser_SFX.set_volume(0.3)

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
        pygame.mixer.Sound.play(self.laser_SFX)
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
        

