import time     # for sleep() and time()
from collections import deque
from pygame.locals import * 

# modules used for Pacba Class
#import ir_sensors
import pacba_movement

class Pacba:

    # FACING DIRECTIONS: x = 0 ; y = 1
    FACING_DIR = [1, 1, -1, -1]

    def __init__(self, serialObject, speed=0):
        "Initialize Pacba Class."
        self.ser = serialObject
        self.curr_axis = 1
        self.curr_facing_dir = 0
        self.speed = speed
        self.positions = deque() #queue
        self.positions.append((0,0))

    def get_current_axis(self):
        "Get Pacba's heading direction."
        return self.curr_axis
    
    def set_current_axis(self, val):
        "Set Pacba's heading direction."
        self.curr_axis = val

    def get_positions(self):
        "Return a list of positions Pacba had been through."
        return self.positions
    
    def get_last_position(self):
        "Return Pacba's most recent position."
        if self.positions:
            return self.positions[-1] # return tuple (x,y)
        
    def add_new_position(self, pos):
        "Add Pacba's new position into list of positions visited."
        self.positions.append(pos)
    
    def run(self, events):
        "Control Pacba Roomba with keyboard inputs to move up and rotate 90 degree left/right."

        speed_bytes = pacba_movement.int_as_2bytes(self.speed)
        # Roomba commands to move
        drive_forward = bytearray([137] + speed_bytes + [128, 0])
        rotate_directions = { "LEFT": bytearray([137] + speed_bytes + [0, 1]), #ccw
                        "RIGHT": bytearray([137] + speed_bytes + [255, 255])} #cw     

        # Pacba's initial position is last position reached
        pos = list(self.get_last_position())
        
        # Travelling time in forward direction
        time_travelled = 0.0 #sec

        for event in events:
            if event.type == KEYDOWN: 
                if event.key == K_UP or event.key == K_w:
                    print("Driving FORWARD")
                    self.ser.write(drive_forward)
                    start_driving_time = time.time()
                    pos[self.curr_axis] += (self.speed * (time.time() - start_driving_time) * 
                                            self.FACING_DIR[self.curr_facing_dir % len(self.FACING_DIR)])

                    
                elif event.key == K_LEFT or event.key == K_a:
                    print("turning LEFT")
                    pacba_movement.rotate_90(self.ser, self.speed, rotate_directions["LEFT"], time.time())
                    self.set_current_axis(~self.curr_axis)
                    self.curr_facing_dir -= 1

                elif event.key == K_RIGHT or event.key == K_d:
                    print("turning RIGHT")
                    pacba_movement.rotate_90(self.ser, self.speed, rotate_directions["RIGHT"], time.time())
                    self.set_current_axis(~self.curr_axis)
                    self.curr_facing_dir += 1

            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    print("STOP")
                    self.ser.write(pacba_movement.STOP)
        
        # Update Pacba's position after all events were processed
        self.add_new_position(tuple(pos))



    

