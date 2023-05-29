import pygame
import random

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.asteroid_images = ['graphics/asteroid1.png', 'graphics/asteroid2.png', 'graphics/asteroid3.png']
        self.image = pygame.image.load(random.choice(self.asteroid_images)).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = 5

    def destroy(self):
        if self.rect.y > 999:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        enemy_data = {
            'Brute': {'health': 100, 'speed': 5, 'attack_type': 'simple', 'attack_sound': 'audio/laser_small_001.ogg'},
            'Rogue': {'health': 80, 'speed': 10, 'attack_type': 'burst', 'attack_sound': 'audio/laser_small_001.ogg'},
            'Mage': {'health': 60, 'speed': 6, 'attack_type': 'spread', 'attack_sound': 'audio/laser_small_001.ogg'}
        }
