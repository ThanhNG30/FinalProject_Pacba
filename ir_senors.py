"""
Author: Ryan Fox
PACba Final Project
Module: ir_sensors.py
Description: Provides booleans containing whether or not a virtual wall
or dock force field has been detected with the ir sensors.  Contains a function
to update those booleans, and functions to return them 
"""

# Constants for holding current detection status, initialized to false
# when module is first loaded (the first time it is imported in the process)
virtual_wall_detected = False
dock_force_field_detected = False

# Query command and packets
QUERY_LIST = [149]
INFRARED_CHAR_OMNI = [17]
INFRARED_CHAR_LEFT = [52]
INFRARED_CHAR_RIGHT = [53]
VIRTUAL_WALL = [13]
REQUIRED_PACKETS = INFRARED_CHAR_OMNI + INFRARED_CHAR_LEFT + \
                   INFRARED_CHAR_RIGHT + VIRTUAL_WALL
BYTES_RETURNED = 4 #one for each infrared packet

# IR Character codes which indicate the dock force field, these may also
# indicate one or both buoy's are present as well, but we don't care about those. 
FORCE_FIELD_CHARS = [242, 250, 246, 254, 161, 165 ,169, 173]

def update(ser):
    """
    Updates the virtual_wall_detected and dock_force_field_detected booleans.
    Takes one argument, a pySerial object, which it uses to communicate with the
    Roomba.  
    """
    # Get sensor data.
    ser.write(bytearray(QUERY_LIST + [len(REQUIRED_PACKETS)] + REQUIRED_PACKETS))
    sensors = ser.read(BYTES_RETURNED)

    # Tell python we want to use the module level variables, otherwise it will
    # create local variables with the same name when we assign them.  
    global virtual_wall_detected
    global dock_force_field_detected

    # We want to set these back to False in case they were True last time update
    # was called, we will then check if they should be set to True again.  
    virtual_wall_detected = False
    dock_force_field_detected = False

    # Check for virtual wall
    if sensors[3] == 1:
        virtual_wall_detected = True

    # Check for force field
    for sensor in sensors[0:3]:
        for char in FORCE_FIELD_CHARS:
            if sensor == char:
                dock_force_field_detected = True

def get_virtual_wall_detected():
    """
    Returns True if a virtual wall was detected, False otherwise
    """
    return virtual_wall_detected

def get_dock_force_field_detected():
    """
    Returns True if a dock force field was detected, False otherwise
    """
    return dock_force_field_detected