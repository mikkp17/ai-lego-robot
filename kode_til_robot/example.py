#!/usr/bin/python3.4
import signal

import ev3dev.ev3 as ev3

btn = ev3.Button()

mL = ev3.LargeMotor('outA')
mR = ev3.LargeMotor('outB')

THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED = 25
TURN_SPEED = 80

clL = ev3.ColorSensor('in1')
clR = ev3.ColorSensor('in2')

clL.mode = 'COL-REFLECT'
clR.mode = 'COL-REFLECT'

assert clL.connected, "ColorSensorLeft(ColorSensor) is not connected"
assert clR.connected, "ColorSensorRight(ColorSensor) is not connected"

# colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

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

LINE_COUNTER = 0

while True:
    mL.duty_cycle_sp = BASE_SPEED
    mR.duty_cycle_sp = BASE_SPEED

    if clL.value() <= 20 and clR.value() <= 20:
        mL.duty_cycle_sp = BASE_SPEED
        mR.duty_cycle_sp = 0
		
		while cl1.value() <= 40 or cl2.value() <= 40:
            # keep running while on black line
            print()

        if clR.value() <= 20:
            mL.duty_cycle_sp = 0
            mR.duty_cycle_sp = 0

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
if btn.down:
    mL.duty_cycle_sp = 0
    mR.duty_cycle_sp = 0
    exit()
