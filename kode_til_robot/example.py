#!/usr/bin/python3.4
import signal

import ev3dev.ev3 as ev3

btn = ev3.Button()

mA = ev3.LargeMotor('outA')
mB = ev3.LargeMotor('outB')

THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED = 15
TURN_SPEED = 80

cl1 = ev3.ColorSensor('in1')
cl2 = ev3.ColorSensor('in2')

cl1.mode = 'COL-REFLECT'
cl2.mode = 'COL-REFLECT'

assert cl1.connected, "ColorSensorLeft(ColorSensor) is not connected"
assert cl2.connected, "ColorSensorRight(ColorSensor) is not connected"

# colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

mB.run_direct()
mA.run_direct()

mA.polarity = "normal"
mB.polarity = "normal"


def signal_handler(sig, frame):
    print('Shutting down gracefully')
    mA.duty_cycle_sp = 0
    mB.duty_cycle_sp = 0

    exit(0)


signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

LINE_COUNTER = 0

while True:
    mA.duty_cycle_sp = BASE_SPEED
    mB.duty_cycle_sp = BASE_SPEED
	
    if cl1.value() <= 20 and cl2.value() <= 20:
		if LINE_COUNTER > 0:
			mA.duty_cycle_sp = 0
			mB.duty_cycle_sp = 0
			exit()
		
		if LINE_COUNTER <= 0:
			while cl1.value() <= 40 or cl2.value() <= 40:
				# keep running while on black line
			LINE_COUNTER += 1
		
    if btn.down:
        mA.duty_cycle_sp = 0
        mB.duty_cycle_sp = 0
        exit()

		
		
		