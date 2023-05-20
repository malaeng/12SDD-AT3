import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint):
        super().__init__()
        self.image = pygame.image.load('graphics/racecar2.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 8
        self.max_x_constraint = constraint


    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
    
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
    
    def update(self):
        self.get_input()
        self.constraint()
        

