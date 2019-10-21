#!/usr/bin/python3.4

import ev3dev.ev3 as ev3
from time import sleep

import signal

mA = ev3.LargeMotor('outA')
mB = ev3.LargeMotor('outB')

THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED = 30
TURN_SPEED = 80

#lightSensorLeft = ev3.ColorSensor('in1')
#lightSensorRight = ev3.LightSensor('in2')

#assert lightSensorLeft.connected, "LightSensorLeft(ColorSensor) is not connected"
#assert lightSensorRight.connected, "LightSensorRight(LightSensor) is not conected"

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


while True:
#	sensorLeft = lightSensorLeft.value()
#	sensorRight = lightSensorRight.value()

#	print("sensorLeft: ", sensorLeft, " sensorRight: ", sensorRight)
#	if sensorRight < THRESHOLD_RIGHT:
#		mA.duty_cycle_sp = TURN_SPEED
#	else:
#		mA.duty_cycle_sp = BASE_SPEED


#	if sensorLeft < THRESHOLD_LEFT:
	mB.duty_cycle_sp = BASE_SPEED
#	else:
	mA.duty_cycle_sp = BASE_SPEED
