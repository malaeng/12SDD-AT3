import pygame
import random
from laser import Laser

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.asteroid_images = ['graphics/asteroid1.png', 'graphics/asteroid2.png', 'graphics/asteroid3.png']
        self.image = pygame.image.load(random.choice(self.asteroid_images)).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = 2
        self.health = 200

    def take_damage(self, damage):
        self.health -= damage
        self.image = None # if time: make this flash white instead
        if self.health <= 0:
            self.kill()
        self.image = pygame.image.load(random.choice(self.asteroid_images)).convert_alpha()

    def destroy(self):
        if self.rect.y > 999:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name: str, pos: tuple, screen_height: int, laser_group: pygame.sprite.Group):
        super().__init__()

        self.asteroid_images = ['graphics/asteroid1.png', 'graphics/asteroid2.png', 'graphics/asteroid3.png']
        # All avaliable enemy types
        self.enemy_data = {
            'asteroid': {'health': 300, 'speed': 3, 'attack_type': None, 'cooldown': None, 'attack_sound': None, 'image': random.choice(self.asteroid_images)},
            'fighter': {'health': 100, 'speed': 5, 'attack_type': 'basic', 'cooldown': (800, 1200), 'attack_sound': 'audio/laserSmall_001.ogg', 'image': 'graphics/enemy_fighter.png'},
            'scout': {'health': 80, 'speed': 10, 'attack_type': 'basic', 'cooldown': (700, 1500), 'attack_sound': 'audio/laserSmall_001.ogg', 'image': 'graphics/enemy_scout.png'},
            'science': {'health': 60, 'speed': 6, 'attack_type': 'spread', 'cooldown': (1600, 2000), 'attack_sound': 'audio/laserSmall_001.ogg', 'image': 'graphics/enemy_science.png'}
        }
        self.type = self.enemy_data[name]

        # Graphics
        self.image = pygame.image.load(self.type['image']).convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        
        self.health = self.type['health']
        self.max_health = self.health
        self.screen_height = screen_height
        self.chosen_position = False
        self.move_position = 0

        # Lasers
        # self.lasers = pygame.sprite.Group()
        self.game_laser_group = laser_group
        self.time_shot = 0

        # Audio
        if self.type['attack_sound']:
            self.attack_SFX = pygame.mixer.Sound(self.type['attack_sound'])
            self.attack_SFX.set_volume(0.05)

    
    def move(self):
        if not self.chosen_position: 
            self.move_position = random.randint(20, self.screen_height-20)
            self.chosen_position = True
        else:
            if self.rect.x > self.move_position: self.rect.x -= 1
            elif self.rect.x < self.move_position: self.rect.x += 1
            elif self.rect.x == self.move_position: self.chosen_position = False
        self.rect.y += 1
        if self.rect.y >= self.screen_height:
            self.kill()

    def take_damage(self, damage: int):
        self.health -= damage
        self.image.set_alpha(255*self.health/self.max_health)
        if self.health <= 0: self.kill()

    def shoot(self):
        self.time_shot = pygame.time.get_ticks()
        attack_type = self.type['attack_type']
        if attack_type == 'basic':
            pygame.mixer.Sound.play(self.attack_SFX)
            self.game_laser_group.add(Laser(self.rect.center, (0, 16), self.screen_height))
        elif attack_type == 'burst':
            pass
        elif attack_type == 'spread':
            pygame.mixer.Sound.play(self.attack_SFX)
            self.game_laser_group.add(Laser(self.rect.center, (0, 12), self.screen_height))
            self.game_laser_group.add(Laser(self.rect.center, (-8, 6), self.screen_height))
            self.game_laser_group.add(Laser(self.rect.center, (8, 6), self.screen_height))

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.type['cooldown']:
            if current_time - self.time_shot >= random.randint(self.type['cooldown'][0], self.type['cooldown'][1]):
                self.shoot()
        self.move()
        #self.shoot()
        #self.lasers.update()


