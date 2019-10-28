import signal

import ev3dev.ev3 as ev3

btn = ev3.Button()
mL = ev3.LargeMotor('outA')
mR = ev3.LargeMotor('outB')
THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED = 30
TURN_SPEED = -10

clL = ev3.ColorSensor('in1')
clR = ev3.ColorSensor('in2')
clL.mode = 'COL-REFLECT'

clR.mode = 'COL-REFLECT'
assert clL.connected, "ColorSensorLeft(ColorSensor) is not connected"
assert clR.connected, "ColorSensorRight(ColorSensor) is not connected"

mL.run_direct()
mR.run_direct()
mL.polarity = "normal"
mR.polarity = "normal"


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
        current_direction_print = current_direction
        current_direction = next_direction
        return 1  # Turn around
    elif current_direction_index - next_direction_index == 1 or current_direction_index - next_direction_index == -3:
        current_direction_print = current_direction
        current_direction = next_direction
        return 2  # Turn left
    elif current_direction_index - next_direction_index == -1 or current_direction_index - next_direction_index == 3:
        current_direction_print = current_direction
        current_direction = next_direction
        return 3  # Turn right


def find_direction_index(direction):
    index = 0
    for value in DIRECTIONS:
        if value.lower() == direction.lower():
            return index
        index += 1


DIRECTIONS = ['u', 'r', 'd', 'l']

# solution = ['L', 'd', 'l', 'l', 'l', 'u', 'u', 'u', 'u', 'R', 'R', 'd', 'r', 'U', 'U', 'U', 'U', 'd', 'd', 'd',
#             'l', 'l', 'l', 'd', 'd', 'r', 'U', 'l', 'u', 'R', 'R', 'd', 'r', 'U', 'U', 'U', 'r', 'u', 'L', 'L',
#             'L', 'u', 'l', 'D', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'l', 'l', 'l', 'd', 'd', 'd', 'r', 'U', 'U',
#             'U', 'l', 'u', 'R', 'R', 'd', 'r', 'U', 'U', 'U', 'r', 'u', 'L', 'd', 'd', 'd', 'd', 'l', 'l', 'd',
#             'd', 'd', 'r', 'r', 'u', 'L', 'd', 'l', 'U', 'U', 'U', 'l', 'u', 'R', 'R', 'd', 'r', 'U', 'U', 'U',
#             'r', 'u', 'u', 'L', 'L', 'L', 'r', 'D', 'R', 'u', 'r', 'D']
solution = ['L', 'd']

STATE = 0

current_direction = 'u'

mL.duty_cycle_sp = BASE_SPEED
mR.duty_cycle_sp = BASE_SPEED
on_line = False

while not btn.down:
    while STATE == 0:
        if clL.value() <= 20 and clR.value() <= 20:
            STATE = 1
        if clL.value() <= 60 <= clR.value():
            mL.duty_cycle_sp = TURN_SPEED
        if clL.value() >= 60 >= clR.value():
            mR.duty_cycle_sp = TURN_SPEED
        if clL.value() >= 60 and clR.value() >= 60:
            mL.duty_cycle_sp = BASE_SPEED
            mR.duty_cycle_sp = BASE_SPEED
    if clL.value() >= 60 and clR.value() >= 60 and STATE == 1:
        mL.duty_cycle_sp = BASE_SPEED
        mR.duty_cycle_sp = -20
        STATE = 2
    while STATE == 2:
        print('turning')
        if clR.value() <= 20:
            print('right sensor black')
            on_line = True
        if on_line is True and clR.value() >= 60:
            print('Passed line')
            on_line = False
            mL.duty_cycle_sp = BASE_SPEED
            mR.duty_cycle_sp = BASE_SPEED
            STATE = 0

print('Program finishing')
mL.duty_cycle_sp = 0
mR.duty_cycle_sp = 0
exit()

'''    if cl1.value() <= 20 and cl2.value() <= 20:
        if LINE_COUNTER > 0:
            mA.duty_cycle_sp = 0
            mB.duty_cycle_sp = 0
            exit()

        if LINE_COUNTER <= 0:
            while cl1.value() <= 40 or cl2.value() <= 40:
            # keep running while on black line
                print()
            LINE_COUNTER += 1
'''
