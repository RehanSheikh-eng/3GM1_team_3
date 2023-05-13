import numpy as np
import time
import json
# import Accelerometer

# data = Accelerometer.Accel(sda_pin=1, scl_pin=2)
# data.start

# Acceleration arrays needs to changed to receive on-line data from accelerometer (note: will likely need to subtract acceleration due to gravity from z)
acc_x = [0,1,0,-1,0]
acc_y = [0,0,0,0,0]
acc_z = [0,0,0,0,0]

vel_x = [0,0]
vel_y = [0,0]
vel_z = [0,0]
vel_mag = [0,0]

distance_accel = 0
distance_GPS = 0

on = True
idx = 1

# Variance values for Kalman Filtering
sigma = 1
var_accel = sigma # Accelerometer variance should be increased with time and/or acceleration magnitude
var_GPS = sigma

while on:
    t = 1 # Time step between samples
    time.sleep(t)

    vel_x[1] = vel_x[0] + (0.5 * t * (acc_x[idx-1] + acc_x[idx]))
    vel_y[1] = vel_y[0] + (0.5 * t * (acc_y[idx-1] + acc_y[idx]))
    vel_z[1] = vel_z[0] + (0.5 * t * (acc_z[idx-1] + acc_z[idx]))

    vel_mag[1] = np.sqrt(vel_x[1]**2 + vel_y[1]**2 + vel_z[1]**2)

    distance_accel += 0.5 * t * (vel_mag[0] + vel_mag[1]) # Distance calculated from accelerometer
    distance_GPS += position_GPS[idx-1] - position_GPS[idx] # Distance calculated from GPS - add appropriate variables
    distance_fused = (var_accel*distance_accel + var_GPS*distance_GPS) / (var_accel + var_GPS) # Kalman filtered distance

    vel_x[0] = vel_x[1]
    vel_y[0] = vel_y[1]
    vel_z[0] = vel_z[1]
    vel_mag[0] = vel_mag[1]

    idx += 1
    on = False