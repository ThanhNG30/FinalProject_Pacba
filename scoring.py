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

class Scoring:
    """Class which handles scoring, needs a Pacba object to figure out
    position and detect dock force fields"""
    def __init__(self, pacba: Pacba):
        """Inits a Scoring object, takes a pacba object as an argument."""
        #Need a pacba object to get sensor and position data from
        self.pacba: Pacba = pacba
        #initialize an empty list to store a history of where points have been scored
        self.score_pos_history = []
        #Initialize actual score counter to 0
        self.score_counter = 0

    def update(self):
        """Checks to see if score should be updated, and adds it to history if so"""
        
        if not self.is_near_already_scored():    
            #If theres a force field, add current position to score history
            if self.pacba.ir_sensors.dock_force_field_detected() == True:
                score_pos_history += [self.pacba.get_last_position()]

            #Then update score counter
            self.score_counter += 1

    def is_near_already_scored(self):
        """Checks if roomba is near any place in the history where it has already scored.
        Returns True/False"""

        #Get the Roomba's most up to date x/y position
        current_x, current_y = self.pacba.get_last_position()

        #Uses 2x the dock detection range to determine if this is near an already scored
        #dock.  There is room for improvement to this to better pinpoint the dock
        #position.  
        for x, y in self.score_pos_history:
            if x - DOCK_DETECTION_RANGE * 2 < current_x < x + DOCK_DETECTION_RANGE * 2 \
            and y - DOCK_DETECTION_RANGE * 2 < current_y < y + DOCK_DETECTION_RANGE * 2:
                return True
        return False

    def clear(self):
        """Resets score_counter to 0"""
        self.score_counter = 0

