import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.bottom_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.bottom_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()
