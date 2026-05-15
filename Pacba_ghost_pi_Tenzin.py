#Tenzin Losal
#Ghost: Randomly roams the play area and tries to hit pacba to prevent from winning
#description: The ghost will move within a boxsize and when it encounters a state where it is outside the box,
             #it will stop and rotate counter-clockwise 90 degree and move again by updating its x and y coordinates
             #to 0. Detects if Pacba is caught by sensing if the bumpers were pressed.

"""Overall classmates:Ryan, Jessica, Julia, and Arield helped solidify the Roomba's behavior as the ghost in pacba_game under the supervision of Dr. Robert Pitts"""
"""Julia demonstrated her code for the ghost"""
"""Ryan and Jessica contributed to Roomba's box idea"""

#from pyserial package the serial module for roomba interaction with the program 
import serial
#client to connect to the server
import client
#waiting for some commands
import time

ser = serial.Serial(baudrate=57600, port="/dev/ttyUSB1")  # Linux: dev file

#Full mode
ser.write(bytes([128, 131]))
"""Dr. Pitts pointed the need to use the sleep method"""
time.sleep(3)
#song upon hitting the left or right bumpers
ser.write(bytes([140, 0, 1, 60, 64]))
#song upon hitting both bumpers both left and right
ser.write(bytes([140, 1, 2, 71, 32, 71, 64]))

class Bots:
    #create an instance for ser interaction
     """Ryan helped identify bugs here"""
     def __init__(self, serial_port, current_x=0, current_y=0):
        self.ser=serial_port
        self.current_x=current_x
        self.current_y=current_y

    #for sensing bumper interaction
     def bumpers_pressed(self):
        #read bumper sensor
        self.ser.write(bytes([142,7]))
        data =self.ser.read(1)
        bits=data[0]

        #when either one of the left and right bumpers pressed, play the corresponding song from 140 opcode(song# 0)
        if (bits==0b00000010) or (bits==0b00000001):
            self.ser.write(bytes([141, 0]))
            return True
            #when both bumpers pressed, play the corresponding song(song# 1)
        if (bits==0b00000011):
            self.ser.write(bytes([141, 1]))
            return True
         "Dr.Pitts added the return false to detect the Roomba bumpers more efficiently" 
        return False

     def move(self):
         """Ryan and Dr.Pitts helped with the indentation error"""
         """Dr. Pitts suggested I change the conditional operators here from !="""
         #if the roomba position for its x or y values are below the corresponding max values for the box 
         if self.current_x<=MAX_X and self.current_y<=MAX_Y:
              #drive straight until the x or y values are more than maximum value for the box coordinates
              self.ser.write(bytes([137, 0, 128, 0, 0]))
              #increment the the position value by 75 in mm
              self.current_x+=75
              self.current_y+=75
         else:
              #stop and then turn 90 degree counter-clockwise
              self.ser.write(bytes([137, 0, 0, 0, 0]))
              #velocity 128mm/s to turn 90 degree
              self.ser.write(bytes([137, 0, 128, 0, 1]))
              #wait for rotation time
              time.sleep(1.45) #takes 1.45 seconds with the velocity to turn 90 degree 
              #stops the rotation 
              self.ser.write(bytes([137, 0, 0, 0, 0]))
              #update roomba coordinates
              self.current_x=0
              self.current_y=0

"""Ryan suggested I use constants for box size"""
#Constants for x and y box axis
#initialized to 500mm 500 x 500, box size 2500mm^2
MAX_X=500
MAX_Y=500

#Instance for bumpers for ghost object
ghost=Bots(ser)

"""Arield helped with the client.connect() and client.run() for the server connection"""
#connect to client
client.connect()
#needs to check the roomba movement and position all the time. 
while True:
     #ghost movement function called 
     ghost.move()
     
     #if both bumpers for ghost pressed display the following message.
     if ghost.bumpers_pressed()!= False:
          print("Ghost caught Pacba!")
     client.run(ghost.bumpers_pressed())
