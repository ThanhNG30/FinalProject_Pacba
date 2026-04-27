import serial   # PySerial: https://pypi.python.org/pypi/pyserial
import time     # for sleep() and time()
import sys      # for exit()
import pygame
import math



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
# 
drive_straight = ser.write(bytearray([137, 0, 0, 0, 0]))
turn_left = ser.write(bytearray([137, 0 , 185, 0, 1]))#ccw
turn_right = ser.write(bytearray([137, 0, 185, 255, 255]))#cw
stop = ser.write(bytearray([137, 0, 0, 0, 0]))
left_k_pressed = False
right_k_pressed = False

# Keep a counter to help control timing
time = 0
spinning_time = ??
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_k_pressed = True
                spinning_time = 
            elif event.key == pygame.K_RIGHT:
                right_k_pressed = True
                spinning_time = 
    if time ?? spinning_time
        #stop
    if time ?? spinning_time
        #spinning
    time += 1
ser.close()
