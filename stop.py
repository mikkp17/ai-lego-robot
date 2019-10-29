import ev3dev.ev3 as ev3

mL = ev3.LargeMotor('outA')
mR = ev3.LargeMotor('outB')

assert mL.connected, "Left motor is not connected"
assert mR.connected, "Right motor is not connected"

mR.run_direct()
mL.run_direct()

mL.polarity = "normal"
mR.polarity = "normal"

mL.duty_cycle_sp = 0
mR.duty_cycle_sp = 0
exit()
