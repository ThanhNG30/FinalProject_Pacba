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
drive_forward = bytearray([137, 0, 100, 128, 0])
turn_left = bytearray([137, 0 , 100, 0, 1])#ccw
turn_right = bytearray([137, 0, 100, 255, 255])#cw
stop = bytearray([137, 0, 0, 0, 0])
left_k_pressed = False
right_k_pressed = False
#for keyboard
pygame.init()

# Keep a counter to help control timing
time = 0
spinning_time = 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_LEFT:
                left_k_pressed = True
            elif event.key == pygame.K_RIGHT:
                right_k_pressed = True
            elif event.key == pygame.K_UP:
                ser.write(drive_forward)
        if stop_time > time:
            if left_k_pressed = True:
                ser.write(turn_left)
                time +=1
            elif right_k_pressed = True:
                ser.write(turn_right)
                time +=1
        elif stop_time == time:
            ser.write(stop)
        
        
    time += 1
    stop_time +=1
ser.close()
