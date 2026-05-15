import time     # for sleep() and time()
import pygame
from collections import deque
from pygame.locals import * 

# modules used for Pacba Class
from ir_sensors import IR_Sensors
import pacba_movement

class Pacba:

    # FACING DIRECTIONS: x = 0 ; y = 1 -Jess
    FACING_DIR = [1, 1, -1, -1]

    def __init__(self, serialObject, speed=0):
        "Initialize Pacba Class."
        self.ser = serialObject
        self.speed = speed

        # x-axis (left/right) = 0, y-axis (front/back) = 1 -Jess
        self.curr_axis = 1
        # Index in the FACING_DIR list, and represents
        # positive/negative value that the Pacba is moving towards -Jess
        self.curr_facing_dir = 0

        # Stores the path that Pacba has moved through -Jess
        self.positions = deque() #queue
        self.positions.append((0,0)) # starts at origin

        # When Pacba starts driving -Jess
        self.driving_time_start = 0
        # Whether Pacba is still driving -Jess
        self.is_driving = False

        # Added a line to initiliaze the IR_Sensors component -Ryan
        self.ir_sensors = IR_Sensors(self)

    # def get_current_axis(self):
    #     "Get Pacba's moving direction."
    #     return self.curr_axis
    
    # def set_current_axis(self, val):
    #     "Set Pacba's moving direction."
    #     self.curr_axis = val

    def get_positions(self):
        "Return a list of positions Pacba had been through."
        return self.positions
    
    def get_last_position(self):
        "Return Pacba's last position."
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
        distance_travelled = 0

        # Handle forward key pressed separately so that it updates position
        # while key is being held down.
        keys = pygame.key.get_pressed() # get list of keys pressed in that moment
        if (keys[K_UP] or keys[K_w]) \
        and not self.ir_sensors.virtual_wall_detected():
            if not self.is_driving:
                self.driving_time_start = time.time()
                self.is_driving = True
                self.ser.write(drive_forward)
            print("Driving FORWARD")
                    
        elif (keys[K_LEFT] or keys[K_a]):
            print("turning LEFT")
            pacba_movement.rotate_90(self.ser, self.speed, rotate_directions["LEFT"], time.time())
            self.curr_axis = ~self.curr_axis
            self.curr_facing_dir -= 1
        
        elif (keys[K_RIGHT] or keys[K_d]):
            print("turning RIGHT")
            pacba_movement.rotate_90(self.ser, self.speed, rotate_directions["RIGHT"], time.time())
            self.curr_axis = ~self.curr_axis
            self.curr_facing_dir += 1

        if (not keys[K_UP] or not keys[K_w])\
        and self.is_driving:
            self.is_driving = False
            self.ser.write(pacba_movement.STOP)
            distance_travelled = (self.speed * (time.time() - self.driving_time_start) * 
                                    self.FACING_DIR[self.curr_facing_dir % len(self.FACING_DIR)])
            print("Distance calculated = ", distance_travelled)
            print("STOP")


        # for event in events:
        #     # # Travelling time in straight direction
        #     # start_driving_time = time.time() #sec

        #     if event.type == KEYDOWN: 
        #         # Appended an "and not" condition to prevent forward movement 
        #         # when a virtual wall is detected -Ryan
        #         if (event.key == K_UP or event.key == K_w) \
        #         and not self.ir_sensors.virtual_wall_detected():
        #             if not self.is_driving:
        #                 self.driving_time_start = time.time()
        #                 self.is_driving = True
        #                 self.ser.write(drive_forward)

        #             print("Driving FORWARD")
                    
        #         elif event.key == K_LEFT or event.key == K_a:
        #             print("turning LEFT")
        #             pacba_movement.rotate_90(self.ser, self.speed, rotate_directions["LEFT"], time.time())
        #             self.curr_axis = ~self.curr_axis
        #             self.curr_facing_dir -= 1
        #             break

        #         elif event.key == K_RIGHT or event.key == K_d:
        #             print("turning RIGHT")
        #             pacba_movement.rotate_90(self.ser, self.speed, rotate_directions["RIGHT"], time.time())
        #             self.curr_axis = ~self.curr_axis
        #             self.curr_facing_dir += 1
        #             break

        #     elif event.type == KEYUP:
        #         if event.key == K_UP or event.key == K_w:
        #             self.is_driving = False
        #             self.ser.write(pacba_movement.STOP)
        #             distance_travelled = (self.speed * (time.time() - self.driving_time_start) * 
        #                             self.FACING_DIR[self.curr_facing_dir % len(self.FACING_DIR)])
        #             print("Distance calculated = ", distance_travelled)
        #             print("STOP")

            # Update Pacba's current position
            pos[self.curr_axis] += distance_travelled
        
        # Update Pacba's position after all events were processed
        self.add_new_position(tuple([int(i) for i in pos]))



    

