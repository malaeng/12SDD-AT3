import pygame
import time
import random
import math

pygame.init()

display_width = 800
display_height = 600


road1 = (112, 108, 108)
green1 = (0, 200, 0)

roadcols = [(112, 108, 108), (112, 80, 80)]

car_z = 30

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pseudo 3D Road Testing')
clock = pygame.time.Clock()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60)

        # print(math.sin(20.0 * (1-display_height/2) ** 2 + car_z * 0.1) > 0.0)


        # pygame.draw.polygon(gameDisplay, road1, [(0, display_height), (display_width, display_height), (0.51*display_width, 0.5*display_height), (0.49*display_width, 0.5*display_height)])
        segments = 2
        angle = 70
        offset = 100
        h = display_height / 2 / segments
        for i in range(segments):
            pygame.draw.polygon(gameDisplay, roadcols[i%2==0], [
                ((offset+h/math.tan(angle))*i, display_height-h*i),
                (display_width-(h/math.tan(angle))*i, display_height-h*i),  
                (display_width-(h/math.tan(angle))*(i+1), display_height-h*(i+1)),
                ((offset+h/math.tan(angle))*(i+1), display_height-h*(i+1))])


main()
pygame.quit()
quit()