import serial   # PySerial: https://pypi.python.org/pypi/pyserial
import time     # for sleep() and time()
import sys      # for exit()
import pygame   # for keyboard inputs
from pygame.locals import * 

# Roomba command to stop
STOP = bytearray([137, 0, 0, 0, 0])

# Time takes to rotate a 90 degree angle is computed accordingly from
# the Roomba's speed.
# Roomba's rotation time for 90 degree angle
TIME_ROTATE_90 = 1.875 # sec at the speed 100

# FUNCTION DEFINITIONS
def rotate_90(serialObj, direction, stop_time):
    "Control Roomba's rotation clockwise/counter-clockwise to be 90 degree."
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

def start_pygame(width, height):
    "Initialize Pygame modules and set up Pygame screen."
    # Initialize Pygame
    pygame.init()  

    # Set up Pygame screen
    screen_size = (width, height)  # pixels
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Roomba Control')

    # Update and display screen buffer
    pygame.display.update()    

def drive(serialObj):
    "Control Pacba Roomba with keyboard inputs to move up and rotate 90 degree left/right."
    for event in pygame.event.get():
        if event.type == KEYDOWN: 
            if event.key == K_UP:
                print("Key UP pressed")
                serialObj.write(drive_forward)
            elif event.key == K_LEFT:
                print("Key LEFT pressed")
                rotate_90(serialObj, rotate_directions["LEFT"], time.time() + 1.875)
            elif event.key == K_RIGHT:
                print("Key RIGHT pressed")
                rotate_90(serialObj, rotate_directions["RIGHT"], time.time() + 1.875)
        elif event.type == KEYUP:
            if event.key == K_UP:
                print("Key UP released")
                serialObj.write(STOP)

# Roomba's speed
speed = int_as_2bytes(100)

# Roomba commands to move
drive_forward = bytearray([137] + speed + [128, 0])

rotate_directions = { "LEFT": bytearray([137] + speed + [0, 1]), #ccw
                      "RIGHT": bytearray([137] + speed + [255, 255])} #cw 



