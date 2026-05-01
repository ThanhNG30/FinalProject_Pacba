"""
Author: Ryan Fox
PACba Final Project
Module: scoring.py
Description: Module which tracks/updates scoring information.  It keeps a
history of where docks have been detected to ensure they aren't scored twice.
"""

import ir_sensors
import position

#Consants
DOCK_DETECTION_RANGE = 500 #In mm, actual tested range is a little below this.  

#initialize an empty list to store a history of where points have been scored
score_pos_history = []

#Keep track of actual score
score_counter = 0

def update():
    """Checks to see if score should be updated, and adds it to history if so"""
    
    if not is_near_already_scored():    
        #If theres a force field, add current position to score history
        if ir_sensors.dock_force_field_detected == True:
            score_pos_history += [(position.x, position.y)]

        #Then update score counter
        score_counter += 1

def is_near_already_scored():
    """Checks if roomba is near any place in the history where it has already scored.
    Returns True/False"""

    for x, y in score_pos_history:
        if x - 1000 < position.x < x + 1000 and y - 1000 < position.y < y + 1000:
            return True
    return False

def clear():
    """Resets score_counter to 0"""
    score_counter = 0

