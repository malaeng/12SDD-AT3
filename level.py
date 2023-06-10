import pygame, random
from menu import Menu, Button
from enemy import Enemy

class Level:
    def __init__(self, screen_size: tuple, title: str, text: str, asteroids: int, fighters: int, scouts: int, sciences: int, difficulty: int):
        self.screen_size = screen_size
        self.title = title
        self.line_max_length = 35
        self.text_lines = self.get_lines(text)

        self.intro_menu = Menu(
            size =  (2*self.screen_size[0]/3, 2*self.screen_size[1]/3),
            title_size = 25,
            parent_surface_dimensions= screen_size,
            colour = '#fbf5ef',
            alpha = 200,
            title = self.title,
            text = [(line, 16) for line in self.text_lines],
            buttons = [Button(300, 100, "Start")],
            stack = True
        )
        self.intro_done = False

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
        self.total_num_enemies = len(self.all_enemies)

        self.current_enemies = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()

        self.spawn_cooldown = difficulty * 2000
        self.time_spawned = 0

    def get_lines(self, text: str) -> list:
        line_list = []
        line = ""
        line_length = 0
        split = text.split()
        for word in split:
            if len(word) + line_length <= self.line_max_length:
                line += word + " "
                line_length += len(word)+1
            else:
                line_list.append(line)
                line_length = len(word)+1
                line = word + " "
        line_list.append(line)
                
        return line_list

    def spawn_handler(self, SFX_on):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_spawned >= self.spawn_cooldown and len(self.all_enemies) > 0:
            self.spawn_enemy(self.all_enemies[0])
            self.all_enemies.pop(0)
        self.current_enemies.update(SFX_on)

    def spawn_enemy(self, enemy_class):
        self.time_spawned = pygame.time.get_ticks()
        spawn_x = random.randint(0, self.screen_size[0])
        self.current_enemies.add(Enemy(enemy_class, (spawn_x, -20), self.screen_size[1], self.enemy_lasers))

    def update(self, SFX_on):
        self.spawn_handler(SFX_on)
        self.enemy_lasers.update()
        self.current_enemies.update(SFX_on)