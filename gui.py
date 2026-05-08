import pygame   # for keyboard inputs
from pygame.locals import * 

#Constants
BACKGROUND_COLOR = (255,255,255) #RGB White
SCORE_COLOR = (0,255,0) #RGB Green
SCORE_FONT_SIZE = 32

class GUI:
    """Class for controlling the GUI display"""

    def __init__(self, screen_width, screen_height, phys_width, phys_height):
        """Inits a GUI object, takes 4 arguments, a screen size
        and the dimensions of a physical play area both as width, height """
        
        #Set size of display screen in pixels
        self._screen_width = screen_width
        self._screen_height = screen_height

        #Set physical size of play area, used to scale co-ordinates to gui
        self._phys_width = phys_width
        self._phys_height = phys_height

        # Initialize Pygame
        pygame.init()  

        # Set up Pygame screen
        
        self._screen = pygame.display.set_mode(self._screen_width, self.screen_height)
        pygame.display.set_caption('Roomba Control')

        # Create a font for score
        self._score_font = pygame.font.Font(size=SCORE_FONT_SIZE)

        # Update and display screen buffer
        pygame.display.update()

    def get_events(self):
        return pygame.event.get()

    def update(self,score):
        """Updates the ui with current roomba position, detected walls, scores, etc"""
        #get the surface from pygame
        self._screen = pygame.display.get_surface()

        #Clear the screen
        self._screen.fill(BACKGROUND_COLOR)

        #DRAW ROOMBA POSITION/WALLS/ETC (possibly separate functions)

        #For now this just displays the current score in the ui -Ryan
        score_text = self._score_font.render(f"Score: {score}", True, SCORE_COLOR)
        score_rect = score_text.get_rect(topright=(self._screen.get_width() - 10, 10))
        self._screen.blit(score_text, score_rect)

        #We call .flip at end to actaully display the updated screen
        pygame.display.flip()

    def get_screen_coords_from_physical_coords(self,phys_x, phys_y):
        """Returns screen coordinates (in pixels) from physical coordinates"""

        #Scale coordinates using screen and physical dimensions set in init
        screen_x = phys_x * self._screen_width / self._phys_width
        screen_y = phys_y * self._screen_height / self._phys_height

        return screen_x, screen_y
