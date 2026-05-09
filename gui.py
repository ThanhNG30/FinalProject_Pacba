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
        
        #Set size of display screen in pixels -Jess
        self._screen_width = screen_width
        self._screen_height = screen_height

        #Set physical size of play area, used to scale co-ordinates to gui -Ryan
        self._phys_width = phys_width
        self._phys_height = phys_height

        # Initialize Pygame -Jess
        pygame.init()  

        # Manage UI elements
        # Reference: https://pygame-gui.readthedocs.io/en/latest/quick_start.html 
        #self.manager = pygame.UIManger((self._screen_width, self._screen_height), theme_path="pacba_theme.json")

        #self.start_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='Start', manager=self.manager)

        # Set up Pygame screen -Jess
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption('Roomba Control')

        # Create an image to display Pacba
        self._pacba_img = pygame.image.load('pacman.jgp')

        # Create a font for score -Ryan
        self._score_font = pygame.font.Font(size=SCORE_FONT_SIZE)

        # Update and display screen buffer -Ryan
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
        self._screen.blit(self._pacba_img, (50,50))

        #For now this just displays the current score in the ui -Ryan
        score_text = self._score_font.render(f"Score: {score}", True, SCORE_COLOR)
        score_rect = score_text.get_rect(topright=(self._screen.get_width() - 10, 10))
        self._screen.blit(score_text, score_rect)

        #We call .flip at end to actually display the updated screen
        pygame.display.flip()

    def get_screen_coords_from_physical_coords(self, phys_x, phys_y):
        """Returns screen coordinates (in pixels) from physical coordinates"""

        #Scale coordinates using screen and physical dimensions set in init
        screen_x = phys_x * self._screen_width / self._phys_width
        screen_y = phys_y * self._screen_height / self._phys_height

        return screen_x, screen_y
    
    def setup(self):
        


    
