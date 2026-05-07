"""
Author: Ryan Fox
PACba Final Project
Module: scoring.py
Description: Provies a Scoring class which tracks/updates scoring information.  
It keeps a history of where docks have been detected to ensure they aren't 
scored twice.
"""

from pacba import Pacba #Imported so type hints / vs code intellisense will work

#Consants
DOCK_DETECTION_RANGE = 500 #In mm, actual tested range is a little below this.

DISPLAY_TEXT = bytearray([164]) #Roomba LED display text command
DISPLAY_LEN = 4 #Roomba LED display size

class Scoring:
    """Class which handles scoring, needs a Pacba object to figure out
    position and detect dock force fields"""
    def __init__(self, pacba: Pacba):
        """Inits a Scoring object, takes a pacba object as an argument."""
        #Need a pacba object to get sensor and position data from
        self._pacba: Pacba = pacba
        #initialize an empty list to store a history of where points have been scored
        self._score_pos_history = []
        #Initialize actual score counter to 0
        self._score_counter = 0
        #Set initial led score display
        self.led_display_score()

    def update(self):
        """Checks to see if score should be updated, and adds it to history if so"""
        
        if not self.is_near_already_scored():    
            #If theres a force field, add current position to score history
            if self._pacba.ir_sensors.dock_force_field_detected() == True:
                self._score_pos_history += [self._pacba.get_last_position()]

            #Then update score counter
            self._score_counter += 1

            #Then update led score display, note this is inside the conditional
            #so score is only updated on score change, which means when it changes
            #elsewhere it needs to called as well
            self.led_display_score()


    def is_near_already_scored(self):
        """Checks if roomba is near any place in the history where it has already scored.
        Returns True/False"""

        #Get the Roomba's most up to date x/y position
        current_x, current_y = self._pacba.get_last_position()

        #Uses 2x the dock detection range to determine if this is near an already scored
        #dock.  There is room for improvement to this to better pinpoint the dock
        #position.  
        for x, y in self._score_pos_history:
            if x - DOCK_DETECTION_RANGE * 2 < current_x < x + DOCK_DETECTION_RANGE * 2 \
            and y - DOCK_DETECTION_RANGE * 2 < current_y < y + DOCK_DETECTION_RANGE * 2:
                return True
        return False

    def clear(self):
        """Resets score_counter to 0"""
        self._score_counter = 0
        self.led_display_score()

    def led_display_score(self):
        """Displays the current score on the Pacba's led display"""
        #Get current score counter as a string
        display_score = str(self._score_counter)
        
        #If current score is too short, add leading 0's
        if len(display_score) < DISPLAY_LEN:
            display_score = ("0" * (DISPLAY_LEN - len(display_score))) + display_score

        #Send pacba command to display score
        display_bytes = bytearray(display_score,"ascii")
        self._pacba.ser.write(DISPLAY_TEXT + display_bytes)

    def get_score(self):
        """Returns the current score."""
        return self._score_counter
