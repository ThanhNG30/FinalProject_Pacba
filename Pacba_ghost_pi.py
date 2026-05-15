#Tenzin Losal
#Ghost: randomly roams the play area and tries to hit pacba to prevent from winning
import serial
import client
import time

ser = serial.Serial(baudrate=57600, port="/dev/ttyUSB1")  # Linux: dev file

ser.write(bytes([128, 131]))

time.sleep(3)
#song upon hitting the left or right bumpers
ser.write(bytes([140, 0, 1, 60, 64]))
#song upon hitting both bumpers both left and right
ser.write(bytes([140, 1, 2, 71, 32, 71, 64]))

class Bots:
    #create an instance for ser interaction
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
        if (bits==0b00000010):
            self.ser.write(bytes([141, 0]))
            return True
            #when both bumpers pressed, play the corresponding song(song# 1)
        if (bits==0b00000011):
            self.ser.write(bytes([141, 1]))
            return True

        return False

     def move(self):
         if self.current_x!= MAX_X or self.current_y!=MAX_Y:
              self.ser.write(bytes([137, 200, 0, 128, 0]))
              self.current_x+=75
              self.current_y+=75
         else:
              self.ser.write(bytes([137, 0, 0, 0, 0]))
              self.ser.write(bytes([137, 0, 0, 64, 0]))

#Constants for x and y box axis
MAX_X=500
MAX_Y=500

#Instances for bumpers for both character objects
ghost=Bots(ser)


client.connect()
while True:
     if ghost.current_x<=MAX_X and ghost.current_y<=MAX_Y:
          ghost.move()
     
     #if both bumpers for pacba and ghost pressed display the following message.
     if ghost.bumpers_pressed()!= False:
          print("Ghost caught Pacba!")
     client.run(ghost.bumpers_pressed())
