from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin

import time

run = Pin('GP16', Pin.IN, Pin.PULL_UP)

def update_motors(tim):
    gain = 0.4
    x, y = test_joystick.get_values()
    L = gain*0.9*min(max(x+y,-1),1)**5
    R = gain*0.9*min(max(x-y,-1),1)**5
    L_motor.set_speed(L)
    R_motor.set_speed(R)
    if not run.value():
        L_motor.disable()
        R_motor.disable()
        tim.deinit()


test_joystick = Joystick('GP28', 'GP27')

L_motor = Motor('GP0', 'GP1', 'GP14')
R_motor = Motor('GP2', 'GP3', 'GP15')

L_motor.enable()
R_motor.enable()

tim = Timer()

tim.init(mode=Timer.PERIODIC, freq=50, callback=update_motors)
