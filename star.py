import pygame, random

class Star(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, screen_height: int, screen_width: int):
        super().__init__()

        # Graphics
        self.image = pygame.image.load('graphics/star.png').convert_alpha()
        self.image.set_alpha(random.randint(150, 200))
        self.rect = self.image.get_rect(center = pos)
        
        # Other variables
        self.speed = 1
        self.screen_height = screen_height
        self.screen_width = screen_width

    def update(self):
        # Moves down at a constant rate. 
        self.rect.y += self.speed

        # If the star goes below the screen height, move it back to the top with a new random x-value
        if self.rect.y > self.screen_height:
            rand_x = random.randint(0, self.screen_width)
            self.rect = self.image.get_rect(center = (rand_x, 0))