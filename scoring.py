"""
Author: Ryan Fox
PACba Final Project
Module: scoring.py
Description: Module which tracks/updates scoring information.  It keeps a
history of where docks have been detected to ensure they aren't scored twice.
"""

import ir_sensors
import position

#initialize an empty list to store a history of where points have been scored
score_history = []

def update():
    """Checks to see if score should be updated, and adds it to history if so"""
    
    #TODO: Check whether or not roomba is currently in range of a place it
    #previously scored.  Below code should not run if within range.  

    #If theres a force field, add current position to score history
    if ir_sensors.dock_force_field_detected == True:
        score_history += [(position.x, position.y)]