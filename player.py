"""
Main module for player controlled roomba
"""
#Standard or 3rd party modules
import serial
import sys
import time

#Our modules
import server
from gui import GUI # gui
from pacba import Pacba # class Pacba
from scoring import Scoring


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

# Initialize Pacba
PACBA_SPEED = 100
player = Pacba(serialObject=ser, speed=PACBA_SPEED)

#Score needed to win (number of docks in play)
VICTORY_SCORE = 2

# Initialize scoring module
score = Scoring(player)

#INIT SERVER
NUM_GHOSTS = 4
server.init_server(NUM_GHOSTS)

#INIT PYGAME/GUI
#Physical area size, just set it to 5000 for testing, units should match
#whatever Pacba is providing (mm hopefully) -Ryan
PLAY_AREA_WIDTH = 5000 
PLAY_AREA_HEIGHT = 5000

# Pygame screen size
PYGAME_SCREEN_WIDTH = 500 #px
PYGAME_SCREEN_HEIGHT = 500 #px 

# Init the gui object, which initializes pygame.  
gui = GUI(PYGAME_SCREEN_WIDTH, PYGAME_SCREEN_HEIGHT, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT, player)

#CONSTANTS FOR GAME LOGIC
game_over = False #Set to true when lost
game_won = False #Set to true when won
game_start_time = time.time()
#START GAME LOOP
while not game_over or game_won:
    #CALCULATE CURRENT TICK TIME
    current_tick_time = time.time()

    #CHECK NETWORK MODULE FOR GAME OVER
    server.update_server()
    game_over = server.ghosts_caught

    #RUN/UPDATE IR SENSOR MODULE DATA FOR VIRTUAL WALLS/ DOCK FORCE FIELDS 
    player.ir_sensors.update()

    #RUN INPUT MODULE FOR PLAYER INPUT/MOVEMENT
    #It needs to provide information about whether or not player is moving
    #It should disable forward movement based on virtual wall data from IR
    #sensor module.
    
    # Get events from Pygame
    events = gui.get_events()
    # Player controls Pacba to move forward and turn left/right
    player.run(events)
    new_pos = player.get_last_position()
    print("Pacba is now at: ", new_pos)

    #RUN POSITION MODULE
    #It should update current player position and make it available as
    #x,y co-ordinates, will need info about movement from INPUT MODULE,
    #as well as current tick time
    #Jessica combined this with the input/player movement.  

    #DETERMINE SCORING
    #Uses data from IR sensor module and co-ordinates from position module to
    #determine if a new point has been scored
    score.update()
    if score.get_score() > VICTORY_SCORE:
        game_won = True

    #UPDATE GUI
    #With current position and points scored, if game over display game over
    gui.update(score.get_score(),game_over,game_won)

#AFTER PLAY CLEANUP

#shut down server
server.shutdown_server()

#shut down pygame
gui.shutdown()

#close roomba connection
ser.close()