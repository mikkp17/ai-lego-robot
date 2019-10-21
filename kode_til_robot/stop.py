#!/usr/bin/python3.4
import ev3dev.ev3 as ev3

mA = ev3.LargeMotor('outA')
mB = ev3.LargeMotor('outB')

mB.run_direct()
mA.run_direct()

mA.polarity = "normal"
mB.polarity = "normal"

mA.duty_cycle_sp = 0
mB.duty_cycle_sp = 0
exit()
