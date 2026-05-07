import pygame   # for keyboard inputs
from pygame.locals import * 

#Constants
BACKGROUND_COLOR = (255,255,255) #RGB White
SCORE_COLOR = (0,255,0) #RGB Green

class GUI:

    def __init__(self, width, height):
        "Initialize Pygame modules and set up Pygame screen."
        # Initialize Pygame
        pygame.init()  

        # Set up Pygame screen
        self.screen_size = (width, height)  # pixels
        self._screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Roomba Control')

        # Create a font for score
        self._score_font = pygame.font.Font(size=14)

        # Update and display screen buffer
        pygame.display.update()

    def get_events():
        return pygame.event.get()

    def update(self,score):
        """Updates the ui with current roomba position, detected walls, scores, etc"""
        #get the surface from pygame
        self._screen = pygame.display.get_surface()

        #Clear the screen
        self._screen.fill()

        #DRAW ROOMBA POSITION/WALLS/ETC (possibly separate functions)

        #For now this just displays the current score in the ui -Ryan
        score_text = self._score_font.render(f"Score: {score}", True, SCORE_COLOR)
        score_rect = score_text.get_rect(topright=(self._screen.get_width - 10, 10))
        self._screen.blit(score_text, score_rect)

        #We call .flip at end to actaully display the updated screen
        pygame.display.flip()
