# NOTES:
# I am writing variables in lowerCamelCase and functions in snake_case

import math
import pygame

pygame.init()  # initializes the module

# SECTION 1 - CANVAS AND MAIN FUNCTION

width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System Simulation")

grey = (30, 30, 30)  # dark grey background for space

def main():
    run = True
    clock = pygame.time.Clock()

    while run:  # every loop
        clock.tick(60)  # max 60 fps
        window.fill(grey)  # fill screen black
        pygame.display.update()  # update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()


# SECTION 2 - PLANETS

class planet():
    def __int__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.x_vel = 0
        self.y_vel = 0

        self.sun = False  # don't want to draw orbit of the sun
        self.distance_to_sun = 0
        self.orbit = []



