'''steps needed to convert the simluink model into a python modesl
written by Ana'''
#constants
normalising_gain= 1/10

#get y data ( rotations)
#lowpass filter

#highpass filter
#append to tremor data

#butterworth filter
#normalising gain 0.1

y_joystick_signal= y_joystick_signal *normalising_gain
return y_joystick_signal

#get x data (forward,back motion)
#lowpass filter

#highpass filter
#append to tremor data

#butterworth filter

x_joystick_signal= x_joystick_signal*normalising_gain
return x_joystick_signal
