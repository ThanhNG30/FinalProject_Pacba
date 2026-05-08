#Tenzin Losal
#Ghost: randomly roams the play area and tries to hit pacba to prevent from winning
import pyserial

ser = serial.Serial(baudrate=115200, port="/dev/ttyUSB0")  # Linux: dev file

#song upon hitting the left or right bumpers
ser.write(bytes([140, 0, 1, 60, 64]))
#song upon hitting both bumpers both left and right
ser.write(bytes([140, 1, 2, 71, 32, 71, 64]))

class Bots:
    #create an instance for ser interaction
     def _init_(self, serial_port):
        self.ser=serial_port
        
    #for sensing bumper interaction
    def bumpers_pressed(self):
        #read bumper sensor
        self.ser.write(bytes([142,7]))
        data =self.ser.read(1)
        bits=data[0]

        #when either one of the left and right bumpers pressed, play the corresponding song from 140 opcode(song# 0) 
        if (bits==0b00000010):
            self.ser.write(bytes([141, 0])
        #when both bumpers pressed, play the corresponding song(song# 1)
        if bits==0b00000011:
            self.ser.write(bytes([141, 1])
            return True

#Instances for bumpers for both character objects
ghost=Bots(ser1)
pacba=Bots(ser2)

#if both bumpers for pacba and ghost pressed display the following message.
if ghost.bumpers_pressed()!= False and pacba.bumpers_pressed()!=False:
        print("Ghost caught Pacba!")
