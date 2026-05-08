"""
Author: Ryan Fox
PACba Final Project
Module: ir_sensors.py
Description: Provides an IR_Sensors class, designed to be a sub-component
of the Pacba class.  That class should initialize this one
when created.  
"""

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

class IR_Sensors:
    """Class for handling IR sensor data for a Pacba"""

    def __init__(self, ser):
        """Inits an IR_Sensors object, takes a  serial object"""
        self._ser = ser
        # Constants for holding current detection status, initialized to false
        # when module is first loaded (the first time it is imported in the process)
        self._virtual_wall_detected = False
        self._dock_force_field_detected = False

    def update(self):
        """
        Updates the virtual_wall_detected and dock_force_field_detected booleans.
        """
        # Get sensor data.
        self._ser.write(bytearray(QUERY_LIST + [len(REQUIRED_PACKETS)] + REQUIRED_PACKETS))
        sensors = self._ser.read(BYTES_RETURNED)

        # We want to set these back to False in case they were True last time update
        # was called, we will then check if they should be set to True again.  
        self._virtual_wall_detected = False
        self._dock_force_field_detected = False

        # Check for virtual wall
        if sensors[3] == 1:
            self._virtual_wall_detected = True

        # Check for force field
        for sensor in sensors[0:3]:
            for char in FORCE_FIELD_CHARS:
                if sensor == char:
                    self._dock_force_field_detected = True

    def virtual_wall_detected(self):
        """
        Returns True if a virtual wall was detected, False otherwise
        """
        return self._virtual_wall_detected

    def dock_force_field_detected(self):
        """
        Returns True if a dock force field was detected, False otherwise
        """
        return self._dock_force_field_detected