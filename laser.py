import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, xyspeed: tuple, screen_height: int):
        super().__init__()
        self.image = pygame.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.xyspeed = xyspeed
        self.bottom_constraint = screen_height

        # Rotate the laser if it is moving left or right.
        if self.xyspeed[0] < 0:
            self.image = pygame.transform.rotate(self.image, -45)
        elif self.xyspeed[0] > 0:
            self.image = pygame.transform.rotate(self.image, 45)

    def destroy(self):
        # If the laser has left the screen, kill it.
        if self.rect.y <= -50 or self.rect.y >= self.bottom_constraint + 50:
            self.kill()

    def update(self):
        # update the x and y values 
        self.rect.x += self.xyspeed[0]
        self.rect.y += self.xyspeed[1]

        self.destroy()
