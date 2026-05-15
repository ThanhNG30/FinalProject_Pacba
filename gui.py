import pygame   # for keyboard inputs
from pygame.locals import * 
from pacba import Pacba #Using to track position, need to import for intellisense

#Constants
BACKGROUND_COLOR = (255,255,255) #RGB White
SCORE_COLOR = (0,0,255) #RGB Blue
SCORE_FONT_SIZE = 32
GAME_OVER_COLOR = (255,0,0) #RGB Red
GAME_OVER_FONT_SIZE = 64
GAME_OVER_MESSAGE = "GAME OVER"
VICTORY_COLOR = (0,255,0) #RGB Green
VICTORY_FONT_SIZE = 64
VICTORY_MESSAGE = "VICTORY"
PADDING = 2 #pixels to pad from edge
PACBA_COLOR = (255,255,0) #RGB Yellow
PACBA_RADIUS = 170 #Create 2 radius in mm

class GUI:
    """Class for controlling the GUI display"""

    def __init__(self, screen_width, screen_height, phys_width, phys_height, pacba: Pacba):
        """Inits a GUI object, takes 4 arguments, a screen size
        and the dimensions of a physical play area both as width, height """
        
        #Keep track of the pacba so we can get its position
        self._pacba = pacba

        #Set size of display screen in pixels
        self._screen_width = screen_width
        self._screen_height = screen_height

        #Set physical size of play area, used to scale co-ordinates to gui
        #Maybe not needed in final implementation since we are storing ratios below
        self._phys_width = phys_width
        self._phys_height = phys_height

        #Ratios for width/height
        self._width_ratio = screen_width // phys_width
        self._height_ratio = screen_height // phys_height

        # Initialize Pygame
        pygame.init()  

        # Set up Pygame screen
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption('Roomba Control')

        # Create a font for score, game over, and victory
        self._score_font = pygame.font.Font(size=SCORE_FONT_SIZE)
        self._game_over_font = pygame.font.Font(size=GAME_OVER_FONT_SIZE)
        self._victory_font = pygame.font.Font(size=VICTORY_FONT_SIZE)

        # Update and display screen buffer
        pygame.display.update()

    def shutdown(self):
        """Does any required gui cleanup and shuts down the gui"""
        #Call pygame.quit()
        pygame.quit()

    def get_events(self):
        return pygame.event.get()

    def update(self,score,game_over,game_won):
        """Updates the ui with current roomba position, detected walls, scores, etc"""
        #get the surface from pygame
        self._screen = pygame.display.get_surface()

        #Clear the screen
        self._screen.fill(BACKGROUND_COLOR)

        #DRAW ROOMBA POSITION/WALLS/ETC (possibly separate functions)
        self.display_pacba_position()

        if game_over:
            self.display_game_over()
        
        if game_won:
            self.display_victory()

        #For now this just displays the current score in the ui -Ryan
        score_text = self._score_font.render(f"Score: {score}", True, SCORE_COLOR)
        score_rect = score_text.get_rect(topright=(self._screen.get_width() - PADDING, PADDING))
        self._screen.blit(score_text, score_rect)

        #We call .flip at end to actaully display the updated screen
        pygame.display.flip()

    def get_screen_coords_from_physical_coords(self,phys_x, phys_y):
        """Returns screen coordinates (in pixels) from physical coordinates"""

        #Scale coordinates using screen and physical dimensions set in init
        screen_x = phys_x * self._width_ratio
        screen_y = phys_y * self._height_ratio

        return screen_x, screen_y

    def display_pacba_position(self):
        """Displays the pacba position in the gui."""

        #get pacbas last position and scale it for the screen size
        phys_pos = self._pacba.get_last_position()
        screen_pos = self.get_screen_coords_from_physical_coords(*phys_pos)
        
        #This is scaling off the average of the ratios for play area/screen width/height
        pacba_size = PACBA_RADIUS * ((self._width_ratio + self._height_ratio)//2)

        #Draw a yellow circle where the pacba is
        pygame.draw.circle(self._screen,PACBA_COLOR,screen_pos,pacba_size)


    def display_game_over(self):
        """Displays a game over message"""
        game_over_text = self._game_over_font.render(GAME_OVER_MESSAGE, True, GAME_OVER_COLOR)
        game_over_rect = game_over_text.get_rect(midtop=(self._screen.get_width() // 2, PADDING))
        self._screen.blit(game_over_text, game_over_rect)

    def display_victory(self):
        """Displays a victory message"""
        victory_text = self._victory_font.render(VICTORY_MESSAGE, True, VICTORY_COLOR)
        victory_rect = victory_text.get_rect(midtop=(self._screen.get_width() // 2, PADDING))
        self._screen.blit(victory_text, victory_rect)

