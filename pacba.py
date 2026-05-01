import serial   # PySerial: https://pypi.python.org/pypi/pyserial
import time     # for sleep() and time()
import sys      # for exit()
import pygame
import pacba_movement
import pacba_gui

# Configure serial communication.
#Set for Create 2 baud rate.
#ser = serial.Serial(baudrate=115200, port="COMx")  # Windows: COM port #
#ser = serial.Serial(baudrate=115200, port="/dev/ttyUSB0")  # Linux: dev file
ser = serial.serial_for_url("socket://127.0.0.1:7654")
if ser.isOpen():
    print('Open: ' + ser.portstr)
else:
    sys.exit()
    
# Initialize Roomba.    
ser.write(bytearray([128, 132]))  # full mode (since pick up Roomba to end)
time.sleep(1)

# Pygame screen size
PYGAME_SCREEN_WIDTH = 100 #px
PYGAME_SCREEN_HEIGHT = 100 #px

# Initialize Pygame GUI
pacba_gui.start_pygame(PYGAME_SCREEN_WIDTH, PYGAME_SCREEN_HEIGHT)

speed = 100

# Main function
while True:
    pacba_movement.drive(ser, speed) # drives Pacba from user's keyboard

ser.close()


