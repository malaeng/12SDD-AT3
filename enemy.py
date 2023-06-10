import pygame
import random
from laser import Laser

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name: str, pos: tuple, screen_height: int, laser_group: pygame.sprite.Group):
        super().__init__()

        # Flags and general variables
        self.screen_height = screen_height
        self.chosen_position = False
        self.move_position = 0

        # Enemy type (on initiation, will be set to only one of these)
        self.enemy_data = {
            'asteroid': {
                'health': 300, 
                'speed': 3, 
                'attack_type': None, 
                'cooldown': None, 
                'attack_sound': None, 
                'image': random.choice(['graphics/asteroid1.png', 'graphics/asteroid2.png', 'graphics/asteroid3.png'])},
            'fighter': {
                'health': 100, 
                'speed': 5, 
                'attack_type': 'basic', 
                'cooldown': (800, 1200), 
                'attack_sound': 'audio/laserSmall_001.ogg', 
                'image': 'graphics/enemy_fighter.png'},
            'scout': {
                'health': 80, 
                'speed': 10, 
                'attack_type': 'basic', 
                'cooldown': (700, 1500), 
                'attack_sound': 'audio/laserSmall_001.ogg', 
                'image': 'graphics/enemy_scout.png'},
            'science': {
                'health': 60, 
                'speed': 6, 
                'attack_type': 'spread', 
                'cooldown': (1600, 2000), 
                'attack_sound': 'audio/laserSmall_001.ogg', 
                'image': 'graphics/enemy_science.png'}
        }
        self.type = self.enemy_data[name]

        # Health
        self.health = self.type['health']
        self.max_health = self.health

        # Graphics
        self.image = pygame.image.load(self.type['image']).convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        # Lasers
        # All enemy lasers are stored in a single sprite group in the game class
        self.game_laser_group = laser_group
        self.time_shot = 0

        # Audio
        if self.type['attack_sound']:
            self.attack_SFX = pygame.mixer.Sound(self.type['attack_sound'])
            self.attack_SFX.set_volume(0.5)

        self.explode_SFX = pygame.mixer.Sound('audio/explosionCrunch_000.ogg')
        self.explode_SFX.set_volume(0.6)

    
    def move(self):
        # Pick a random x-value.
        if not self.chosen_position: 
            self.move_position = random.randint(20, self.screen_height-20)
            self.chosen_position = True
        # If one has already been chose, move towards it slowly.
        else:
            if self.rect.x > self.move_position: self.rect.x -= 1
            elif self.rect.x < self.move_position: self.rect.x += 1
            # Once it reaches the x-value, pick a new one
            elif self.rect.x == self.move_position: self.chosen_position = False 

        # Always move downwards.
        self.rect.y += 1

        # If it has gone offscreen, kill it
        if self.rect.y >= self.screen_height:
            self.kill()

    def take_damage(self, damage: int, SFX_on: bool):
        # Takes damage away from health, and sets the alpha (transperency) to the percent of it's max health.
        # If it has no health, kill it.
        self.health -= damage
        self.image.set_alpha(255*self.health/self.max_health)
        if self.health <= 0: 
            self.kill()
            if SFX_on: pygame.mixer.Sound.play(self.explode_SFX)

    def shoot(self, SFX_on: bool):
        # Saves the time that the enemy shot
        self.time_shot = pygame.time.get_ticks()


        attack_type = self.type['attack_type']
        if attack_type == 'basic':
            # Shoots a single laser that moves very fast
            if SFX_on: pygame.mixer.Sound.play(self.attack_SFX)
            self.game_laser_group.add(Laser(self.rect.center, (0, 16), self.screen_height))
        elif attack_type == 'burst':
            # Not implemented, due to time constraints
            pass
        elif attack_type == 'spread':
            # Shoots 3 slower lasers that spread out
            if SFX_on: pygame.mixer.Sound.play(self.attack_SFX)
            self.game_laser_group.add(Laser(self.rect.center, (0, 12), self.screen_height))
            self.game_laser_group.add(Laser(self.rect.center, (-8, 6), self.screen_height))
            self.game_laser_group.add(Laser(self.rect.center, (8, 6), self.screen_height))

    def update(self, SFX_on):
        current_time = pygame.time.get_ticks()
        if self.type['cooldown']:
            # Checks that time passed between last shot is greater than a random cooldown value for the enemy class
            if current_time - self.time_shot >= random.randint(self.type['cooldown'][0], self.type['cooldown'][1]):
                self.shoot(SFX_on)
        self.move()


