from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin

import time

Run = Pin('GP16', Pin.IN)

def update_motors(tim):
    L, R = test_joystick.get_values()
    L_motor.set_speed(L)
    if not Run.value():
        tim.deinit()


test_joystick = Joystick('GP28', 'GP27')

L_motor = Motor('GP2', 'GP3', 'GP0', 'GP1', 'GP4')

L_motor.enable()

tim = Timer()

tim.init(mode=Timer.PERIODIC, freq=1000, callback=update_motors)
