"""
Main module for player controlled roomba
"""
#Standard or 3rd party modules
import serial
import sys
import time

#Our modules
import server
import gui
import position
import input
import ir_sensors


#INIT CONNECTION TO PLAYER ROOMBA
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
ser.write(bytearray([128, 131]))  # safe mode
time.sleep(1)  # need to pause after send mode

#INIT SERVER
#server.init()

#INIT PYGAME/GUI
#gui.init()

#CONSTANTS FOR GAME LOGIC
game_over = False #Set to true when loop should terminate
game_start_time = time.time()
#START GAME LOOP
while not game_over:
    #CALCULATE CURRENT TICK TIME
    current_tick_time = time.time()

    #CHECK NETWORK MODULE FOR GAME OVER
    #server.update()
    #game_over = server.is_game_over()

    #RUN/UPDATE IR SENSOR MODULE DATA FOR VIRTUAL WALLS/ DOCK FORCE FIELDS 
    #ir_sensors.update(ser)
    #ir_sensors.virtual_wall_detected
    #ir_sensors.dock_force_field_detected

    #RUN INPUT MODULE FOR PLAYER INPUT/MOVEMENT
    #It needs to provide information about whether or not player is moving
    #It should disable forward movement based on virtual wall data from IR
    #sensor module.
    #input.update(ser)
    #input.turning_left
    #input.turning_right
    #input.moving_forward

    #RUN POSITION MODULE
    #It should update current player position and make it available as
    #x,y co-ordinates, will need info about movement from INPUT MODULE,
    #as well as current tick time
    #x, y = position.update()
    #position.x
    #position.y

    #DETERMINE SCORING
    #Uses data from IR sensor module and co-ordinates from position module to
    #determine if a new point has been scored
    #scoring.update()
    #scoring.score

    #UPDATE GUI
    #With current position and points scored, if game over display game over
    #gui.update()

#AFTER PLAY CLEANUP

#close roomba connection
ser.close()

#shut down server
#server.shutdown()

#shut down pygame?