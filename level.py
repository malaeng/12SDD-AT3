import pygame, random
from menu import Menu, Button
from enemy import Enemy

class Level:
    def __init__(self, screen_size: tuple, title: str, text: str, asteroids: int, fighters: int, scouts: int, sciences: int, difficulty: int):
        self.screen_size = screen_size
        self.title = title
        self.text = text
        self.intro_menu = Menu(
            size =  (2*self.screen_size[0]/3, 2*self.screen_size[1]/3),
            title_size = 40,
            parent_surface_dimensions= screen_size,
            colour = '#fbf5ef',
            alpha = 200,
            title = self.title,
            text = [(self.text, 16)],
            buttons = [Button(300, 100, "Start")],
            stack = True
        )

        self.asteroids = asteroids
        self.fighters = fighters
        self.scouts = scouts
        self.sciences = sciences

        self.all_enemies = []
        for i in range(self.asteroids): self.all_enemies.append('asteroid')
        for i in range(self.fighters): self.all_enemies.append('fighter')
        for i in range(self.scouts): self.all_enemies.append('scout')
        for i in range(self.sciences): self.all_enemies.append('science')
        random.shuffle(self.all_enemies)

        self.current_enemies = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()

        self.spawn_cooldown = difficulty * 2000
        self.time_spawned = 0

    def spawn_handler(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_spawned >= self.spawn_cooldown and len(self.all_enemies) > 0:
            self.spawn_enemy(self.all_enemies[0])
            self.all_enemies.pop(0)
        self.current_enemies.update()

    def spawn_enemy(self, enemy_class):
        self.time_spawned = pygame.time.get_ticks()
        spawn_x = random.randint(0, self.screen_size[0])
        self.current_enemies.add(Enemy(enemy_class, (spawn_x, -20), self.screen_size[1], self.enemy_lasers))

    def update(self):
        self.spawn_handler()
        self.enemy_lasers.update()
        self.current_enemies.update()