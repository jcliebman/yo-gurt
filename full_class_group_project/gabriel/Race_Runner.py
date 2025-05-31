# this is the main file that will execute all the code

import pygame
from Track_Ops import *
from User_Car import *


# Window Setup
WIN_COLOR = (150,150,150)
width = 1440
height = 845
win = pygame.display.set_mode((width, height))
win.fill(WIN_COLOR)
pygame.display.set_caption("Client")
#create font
pygame.font.init()
font = pygame.font.SysFont('roboto', 50)
winfont = pygame.font.SysFont('courier', 100)

# General Constants
X = 0
Y = 1

# Track Constants
LINE_WIDTH = 3
LINE_HEIGHT = 3
BLACK = (0,0,0)

track = Track(win)
track.initialize()

# Car Constants
CAR_WIDTH = 80
CAR_HEIGHT = 80

plrcar = pCar(0,0,CAR_WIDTH,CAR_HEIGHT,"user")


def redrawWindow(win):
    # Fill the window with an image
    win.fill(WIN_COLOR)

    # Draw the player's car
    plrcar.draw(win)

    # Update the display
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               run = False
               pygame.quit()
        redrawWindow(win)
        track.track_draw()

main()
