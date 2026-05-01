import pygame   # for keyboard inputs
from pygame.locals import * 


def start_pygame(width, height):
    "Initialize Pygame modules and set up Pygame screen."
    # Initialize Pygame
    pygame.init()  

    # Set up Pygame screen
    screen_size = (width, height)  # pixels
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Roomba Control')

    # Update and display screen buffer
    pygame.display.update()

def get_events():
    return pygame.events.get()