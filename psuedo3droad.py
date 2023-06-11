# Created by Malachi English, 12/6/2023
# Testing psuedo 3D roads. Ended up scrapping this idea.

import pygame
import time
import random
import math

pygame.init()

display_width = 800
display_height = 600


road1 = (112, 108, 108)
green1 = (0, 200, 0)

roadcols = [(112, 108, 108), (67, 69, 71)]
grasscols = [(0, 200, 0), (0, 160, 0)]
bordercols = [(255, 255, 255), (200, 0, 0)]



gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pseudo 3D Road Testing')
clock = pygame.time.Clock()

def main():
    curve_amount = 0
    curve_change = 0

    car_z = 0
    car_z_change = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    curve_change = -0.01
                if event.key == pygame.K_d:
                    curve_change = 0.01
                if event.key == pygame.K_w:
                    car_z_change = 0.8
                if event.key == pygame.K_s:
                    car_z_change = -0.8

            # doesn't work well when pressing two at a time.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j or event.key == pygame.K_l:
                    curve_change = 0
                if event.key == pygame.K_i or event.key == pygame.K_m:
                    car_z_change = 0     

        # Draw sky

        pygame.draw.polygon(gameDisplay, (200, 213, 227), [
            (0, 0),
            (0, display_height), 
            (display_width, display_height),
            (display_width, 0)
        ])

        # Draw mountains
        pygame.draw.polygon(gameDisplay, (114, 132, 150), [
            (-0.5*curve_amount*car_z, display_height/2),
            (-0.5*curve_amount*car_z+50, display_height/2 - 150),
            (-0.5*curve_amount*car_z+80, display_height/2 - 180),
            (-0.5*curve_amount*car_z+140, display_height/2)
        ])


        # Draw grass
        segments = 500
        h = (display_height / 3 ) * 2 / segments
        car_z += car_z_change
        for i in range(segments):
            pygame.draw.polygon(gameDisplay, grasscols[math.cos(((i/100) ** 3)+car_z) > 0.0], [
                (0, display_height-h*i),
                (display_width, display_height-h*i),
                (display_width, display_height-h*(i+1)),
                (0, display_height-h*(i+1))
            ])

        angle = math.radians(54.0) # convert degrees to radians because trig is done in radians in python
        offset = 100.0 # Distance between road and edge of screen
        
        curve_amount += curve_change
        
        # draw road
        for i in range(segments):
            pygame.draw.polygon(gameDisplay, roadcols[math.cos(((i/100) ** 3)+car_z+30) > 0.0], [
                (offset + curve_amount * ((i/40) ** 2) + (h/math.tan(angle))*i, display_height-h*i),
                (display_width-offset + curve_amount * ((i/40) ** 2) - ((h/math.tan(angle))*i), display_height-h*i),  
                (display_width-offset + curve_amount * ((i/40) ** 2) - ((h/math.tan(angle))*(i+1)), display_height-h*(i+1)),
                (offset + curve_amount * ((i/40) ** 2) +  (h/math.tan(angle))*(i+1), display_height-h*(i+1))])

        border_length = 20
        for i in range(segments):
            pygame.draw.polygon(gameDisplay, bordercols[math.cos(((i/100) ** 3)+car_z+30) > 0.0], [
                (offset + curve_amount * ((i/40) ** 2) + (h/math.tan(angle))*i, display_height-h*i),
                (offset + curve_amount * ((i/40) ** 2) + (h/math.tan(angle))*(i+10), display_height-h*i),  
                (offset + curve_amount * ((i/40) ** 2) + (h/math.tan(angle))*(i+11), display_height-h*(i+1)),
                (offset + curve_amount * ((i/40) ** 2) +  (h/math.tan(angle))*(i+1), display_height-h*(i+1))])
            
        pygame.display.update()
        clock.tick(60)


main()
pygame.quit()
quit()