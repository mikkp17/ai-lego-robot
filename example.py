import signal
import time

import ev3dev.ev3 as ev3

btn = ev3.Button()

mL = ev3.LargeMotor('outA')
mR = ev3.LargeMotor('outB')
mL.run_direct()
mR.run_direct()
mL.polarity = "normal"
mR.polarity = "normal"

BASE_SPEED = 40
CORRECTION_SPEED = 20
TURN_SPEED = -20
REVERSE_SPEED = -30

sL = ev3.ColorSensor('in1')
sR = ev3.ColorSensor('in2')
sL.mode = 'COL-REFLECT'
sR.mode = 'COL-REFLECT'
assert sL.connected, "ColorSensorLeft(ColorSensor) is not connected"
assert sR.connected, "ColorSensorRight(ColorSensor) is not connected"


def signal_handler(sig, frame):
    print('Shutting down gracefully')
    mL.duty_cycle_sp = 0
    mR.duty_cycle_sp = 0
    exit(0)


signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')


def calculate_direction(next_direction):
    global current_direction
    current_direction_index = find_direction_index(current_direction)
    next_direction_index = find_direction_index(next_direction)

    if current_direction_index == next_direction_index:
        return 0  # Go straight
    elif abs(current_direction_index - next_direction_index) == 2:
        current_direction = next_direction
        return 1  # Turn around
    elif current_direction_index - next_direction_index == 1 or current_direction_index - next_direction_index == -3:
        current_direction = next_direction
        return 2  # Turn left
    elif current_direction_index - next_direction_index == -1 or current_direction_index - next_direction_index == 3:
        current_direction = next_direction
        return 3  # Turn right


def find_direction_index(direction):
    index = 0
    for value in DIRECTIONS:
        if value.lower() == direction.lower():
            return index
        index += 1


def increment_counter():
    global counter_index
    global finished
    counter_index += 1
    print(counter_index)
    print(len(solution))
    if counter_index >= len(solution):
        finished = True


DIRECTIONS = ['u', 'r', 'd', 'l']

solution_string = 'uurdlrl'
# 'lllldlluRRUdRRRdrUUruulldRRdldlluLuulldRurDDullDRdRRRdrUUruurrdLulDulldRddlllldlluRRRRRdrUUdlllluurDldRRRdrU'
solution = list(solution_string)
STATE = 0
current_direction = 'u'
counter_index = 0
mL.duty_cycle_sp = BASE_SPEED
mR.duty_cycle_sp = BASE_SPEED
on_line = False
direction = -1
finished = False

while not finished:
    while STATE == 0:
        if sL.value() <= 20 and sR.value() <= 20:
            mL.duty_cycle_sp = BASE_SPEED
            mR.duty_cycle_sp = BASE_SPEED
            STATE = 1
        if sL.value() <= 60 <= sR.value():
            mL.duty_cycle_sp = TURN_SPEED
            mR.duty_cycle_sp = BASE_SPEED
        elif sL.value() >= 60 >= sR.value():
            mR.duty_cycle_sp = TURN_SPEED
            mL.duty_cycle_sp = BASE_SPEED
        elif sL.value() >= 60 and sR.value() >= 60:
            mL.duty_cycle_sp = BASE_SPEED
            mR.duty_cycle_sp = BASE_SPEED
    if sL.value() >= 60 and sR.value() >= 60 and STATE == 1:
        direction = calculate_direction(solution[counter_index])
        print(solution[counter_index])
        increment_counter()
        STATE = 2
    while STATE == 2:
        print('commencing turning')
        if direction == 0:
            mR.duty_cycle_sp = BASE_SPEED
            mL.duty_cycle_sp = BASE_SPEED
            STATE = 0
        elif direction == 1:
            # do nothing
            print('should turn around')
        elif direction == 2:
            print('Direction = 2')
            STATE = 3
            mL.duty_cycle_sp = TURN_SPEED
            mR.duty_cycle_sp = BASE_SPEED
            while STATE == 3:
                if sL.value() <= 20:
                    on_line = True
                if on_line is True and sL.value() >= 60:
                    print('passed line')
                    on_line = False
                    mL.duty_cycle_sp = BASE_SPEED
                    mR.duty_cycle_sp = BASE_SPEED
                    STATE = 0
        elif direction == 3:
            print('Direction = 3')
            STATE = 3
            mR.duty_cycle_sp = TURN_SPEED
            mL.duty_cycle_sp = BASE_SPEED
            while STATE == 3:
                if sR.value() <= 20:
                    on_line = True
                if on_line is True and sR.value() >= 60:
                    print('passed line')
                    on_line = False
                    mL.duty_cycle_sp = BASE_SPEED
                    mR.duty_cycle_sp = BASE_SPEED
                    STATE = 0

print('Program finishing')
mL.duty_cycle_sp = 0
mR.duty_cycle_sp = 0
exit()
