import time     # for sleep() and time() 
import math     # for pi

# Distance between Roomba's wheels according to the documentation
WHEELS_DISTANCE = 235 # mm

# Roomba command to stop
STOP = bytearray([137, 0, 0, 0, 0])

# Time takes to rotate a 90 degree angle is computed accordingly from
# the Roomba's speed.
# Roomba's rotation time for 90 degree angle
# TIME_ROTATE_90 = 1.875 # sec at the speed 100


# FUNCTION DEFINITIONS
def get_time_to_rotate(angle, speed):
    """Compute the total time takes for Roomba to rotate in place a certain degree.
    Using the formula: 
    (t = desired angle (radian) * distance between Roomba's wheels (mm) / 2 * speed (mm/sec)"""
    if abs(speed) in range(501):
        angle_in_rad = angle * math.pi / 180
        return (angle_in_rad * WHEELS_DISTANCE) / (2 * abs(speed))

def rotate_90(serialObj, speed, direction, curr_time):
    "Control Roomba's rotation clockwise/counter-clockwise to be 90 degree."
    stop_time = curr_time + get_time_to_rotate(90, speed)
    print("Current time = ", curr_time, "Stop time = ", stop_time)
    serialObj.write(direction)
    while stop_time >= time.time():
        continue
    serialObj.write(bytearray([137, 0, 0, 0, 0]))

def int_as_2bytes(num):
    "Converts 16-bit signed integer to 2 unsigned bytes and returns as list."
    
    # Mask off high bytes.
    low = num & 0xFF

    # Shift high byte(s) down on byte, then
    # mask off any additional high byte(s).
    high = (num >> 8) & 0xFF

    return [high, low]   

#def drive(pacba, serialObj, speed):   
    