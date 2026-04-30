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
pygame.init()    
# Initialize Roomba.    
ser.write(bytearray([128, 132]))  # full mode (since pick up Roomba to end)
time.sleep(1)
# 
drive_straight = bytearray([137, 0, 100, 128, 0])
turn_left = bytearray([137, 0 , 100, 0, 1])#ccw
turn_right = bytearray([137, 0, 100, 255, 255])#cw
stop = bytearray([137, 0, 0, 0, 0])
left_k_pressed = False
right_k_pressed = False

# Keep a counter to help control timing
time = 0
spinning_time = 0
stop_spinning_time = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_LEFT:
                left_k_pressed = True
                spinning_time = time +1  
            elif event.key == pygame.K_RIGHT:
                right_k_pressed = True
                spinning_time = time +1
            elif event.key == pygame.K_UP:
                ser.write(drive_straight)
        if time < spinning_time:
            while left_k_pressed == True:
                ser.write(turn_left)
                if spinning_time == stop_spinning_time:
                    ser.write(stop)
                    spinning_time = 0
                spinning_time +=1
            while right_k_pressed == True:
                ser.write(turn_right) 
                if spinning_time == stop_spinning_time:
                    ser.write(stop)
                    spinning_time = 0
                spinning_time +=1
    time += 1
    stop_spinning_time = time +3
ser.close()
