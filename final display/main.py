# main.py -- put your code here!
from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin
from tim_filter import MovingAverage

xfilter = MovingAverage(10)
yfilter = MovingAverage(10)

run = Pin('GP26', Pin.IN)

test_joystick = Joystick('GP28', 'GP27')

L_motor = Motor('GP0', 'GP1', 'GP14')
R_motor = Motor('GP2', 'GP3', 'GP15')

tim = Timer()

def update_motors(tim):
    if not run.value():
        L_motor.disable()
        R_motor.disable()
        tim.deinit()
    safety = 0.8
    x, y = test_joystick.get_values()
    x = xfilter.update(x)
    y = yfilter.update(y)
    L = safety*0.9*min(max(x+y,-1),1)
    R = safety*0.9*min(max(x-y,-1),1)
    L_motor.set_speed(L)
    R_motor.set_speed(R)

if run.value():
    L_motor.enable()
    R_motor.enable()
    tim.init(mode=Timer.PERIODIC, freq=100, callback=update_motors)

print('Not Running')