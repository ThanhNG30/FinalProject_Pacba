'''
NGOC BAO TRAN NGUYEN
FINAL PROJECT
GHOST MOVEMENT

'''
import serial   # PySerial: https://pypi.python.org/pypi/pyserial
import time     # for sleep() and time()
import sys      # for exit()
import random   # for random distance and directtion
# Configure serial communication.
# Set for Create 1 baud rate.
#ser = serial.Serial(baudrate=57600, port="COM8")  # Windows: COM port #
#ser = serial.Serial(baudrate=57600, port="/dev/ttyUSB0")  # Linux: dev file
ser = serial.serial_for_url("socket://127.0.0.1:7654")  # Simulator

# Print port open or exit.
if ser.isOpen():
    print('Open: ' + ser.portstr)
else:
    sys.exit()
# Initialize Roomba
ser.write(bytearray([128, 131]))
time.sleep(1)  # need to pause after send mode
### Code from Adv Robo Coding Exam
def int_as_2bytes(num):
    "Converts 16-bit signed integer to 2 unsigned bytes and returns as list."
    
    # Mask off high bytes.
    low = num & 0xFF

    # Shift high byte(s) down on byte, then
    # mask off any additional high byte(s).
    high = (num >> 8) & 0xFF

    return [high, low]

# opcode and script
SPEED = 100
DRIVE = [137]
WAIT_DIS = [156]
WAIT_ANGLE = [157]
SCRIPT = [152]
PLAY_SCRIPT = [153]

# rotation
GO_STRAIGHT = [128, 0]
CW = [255, 255]
CCW = [0, 1]

#set up play area
WIDTH = 500
HEIGHT = 500
ANGLE = 90
DISTANCE = (WIDTH + HEIGHT)//2 - 50
STOP = [137, 0, 0, 0, 0]
# song
STORE_SONG = [140]
PLAY_SONG = [141]
DETECTED_VWALL_SONG = [ 1, 2, 70, 32, 70, 32]
ser.write(bytearray(STORE_SONG + DETECTED_VWALL_SONG)) # store song
DETECTED_PACBA_SONG = [ 0, 3, 73, 32, 73, 32, 73, 32]
ser.write(bytearray(STORE_SONG + DETECTED_PACBA_SONG)) # store song

#bumpers
left_bumper_pressed = False
right_bumper_pressed = False
both_bumpers_pressed = False
virtual_wall_detected = False
wall_detected = False
dock_detected = False
#sensor
SEND_SENSOR = [149, 3, 7, 13, 17]
IR_PACKET = [242, 250, 246, 254]
#drive cmd
dis_wait = int_as_2bytes(DISTANCE)
vel_drive = int_as_2bytes(SPEED)
bw_vel_drive = int_as_2bytes(-SPEED)
angle_deg = int_as_2bytes(ANGLE)
drive_forward = DRIVE + vel_drive + GO_STRAIGHT
drive_backward = DRIVE + bw_vel_drive + GO_STRAIGHT
#running script
vir_wall_script = (
    SCRIPT + [21] +
    DRIVE + int_as_2bytes(-150) + GO_STRAIGHT +
    WAIT_DIS + int_as_2bytes(-150) +
    DRIVE + int_as_2bytes(150) + CCW +
    WAIT_ANGLE + int_as_2bytes(180) +
    STOP
)

rd_turn_45deg = (
    SCRIPT + [13] +
    DRIVE + int_as_2bytes(200) + CCW +
    WAIT_ANGLE + int_as_2bytes(45) +
    STOP
)

rd_turn_135deg = (
    SCRIPT + [13] +
    DRIVE + int_as_2bytes(200) + CCW +
    WAIT_ANGLE + int_as_2bytes(135) +
    STOP
)

turn_left_90_script = (
    SCRIPT + [13] +
    DRIVE + int_as_2bytes(200) + CCW +
    WAIT_ANGLE + int_as_2bytes(90) +
    STOP
)

turn_right_90_script = (
    SCRIPT + [13] +
    DRIVE + int_as_2bytes(-200) + CCW +
    WAIT_ANGLE + int_as_2bytes(90) +
    STOP
)
#abc
while True:
    ser.write(bytearray(SEND_SENSOR))
    data = list(ser.read(3))
    print(data)
    bumpers = data[0]
    virtual_wall = data[1]
    dock = data[2]
    
# check data
    if bumpers == 1:
        right_bumper_pressed = True
    elif bumpers == 2:
        left_bumper_pressed = True
    elif bumpers == 3:
        both_bumpers_pressed = True
    if virtual_wall == 1:
        virtual_wall_detected = True

    if virtual_wall_detected == True:
        print("v.wall")
        ser.write(bytearray(PLAY_SONG + [1]))
        ser.write(bytearray(vir_wall_script))
        ser.write(bytearray(PLAY_SCRIPT))
        time.sleep(1)
        virtual_wall_detected = False
    elif both_bumpers_pressed == True:
        ser.write(bytearray(PLAY_SONG + [0]))
        ser.write(bytearray([137, 0, 250, 255, 255]))
        time.sleep(1)
        print("both or pacba")
        both_bumpers_pressed = False
        time.sleep(5)
        ser.write(bytearray(STOP))
    elif left_bumper_pressed == True:
        ser.write(bytearray(turn_right_90_script))#turn right
        ser.write(bytearray(PLAY_SCRIPT))
        print("right")
        time.sleep(1)
        left_bumper_pressed = False
    elif right_bumper_pressed == True:
        ser.write(bytearray(turn_left_90_script))#turn left
        ser.write(bytearray(PLAY_SCRIPT))
        print("left")
        time.sleep(1)
        right_bumper_pressed = False
    elif virtual_wall_detected == False:
        ser.write(bytearray(drive_forward))
        forward_time = random.uniform(1.0, 4.5) # decide how long roomba run
        time.sleep(forward_time)
        print("forward")
        choice = random.choice(["turn_45deg", "turn_135deg"]) 
        if choice == "turn_45deg": 
            ser.write(bytearray(rd_turn_45deg))
            ser.write(bytearray(PLAY_SCRIPT))
            time.sleep(1)
            print("turn 45")
        elif choice == "turn_135deg":
            ser.write(bytearray(rd_turn_135deg))
            ser.write(bytearray(PLAY_SCRIPT))
            time.sleep(1)
            print("turn_135deg")
  
ser.close()    
