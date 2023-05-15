import numpy as np
import time
import json
# import Accelerometer

# data = Accelerometer.Accel(sda_pin=1, scl_pin=2)
# data.start

# Acceleration arrays needs to changed to receive on-line data from accelerometer (note: will likely need to subtract acceleration due to gravity from z)
# acc_x = [0,1,0,-1,0]
# acc_y = [0,0,0,0,0]
# acc_z = [0,0,0,0,0]

# vel_x = [0,0]
# vel_y = [0,0]
# vel_z = [0,0]
# vel_mag = [0,0]

# distance_accel = 0
# distance_GPS = 0

# on = True
# idx = 1

# # Variance values for Kalman Filtering
# sigma = 1
# var_accel = sigma # Accelerometer variance should be increased with time
# var_GPS = sigma

# while on:
#     t = 1 # Time step between samples
#     time.sleep(t)

#     vel_x[1] = vel_x[0] + (0.5 * t * (acc_x[idx-1] + acc_x[idx]))
#     vel_y[1] = vel_y[0] + (0.5 * t * (acc_y[idx-1] + acc_y[idx]))
#     vel_z[1] = vel_z[0] + (0.5 * t * (acc_z[idx-1] + acc_z[idx]))

#     vel_mag[1] = np.sqrt(vel_x[1]**2 + vel_y[1]**2 + vel_z[1]**2)

#     distance_accel += 0.5 * t * (vel_mag[0] + vel_mag[1]) # Distance calculated from accelerometer
#     distance_GPS += position_GPS[idx-1] - position_GPS[idx] # Distance calculated from GPS - add appropriate variables
#     distance_fused = (var_accel*distance_accel + var_GPS*distance_GPS) / (var_accel + var_GPS) # Kalman filtered distance

#     vel_x[0] = vel_x[1]
#     vel_y[0] = vel_y[1]
#     vel_z[0] = vel_z[1]
#     vel_mag[0] = vel_mag[1]

#     if var_accel < 100: # to prevent numerical overflow
#         var_accel += 1 # to account for drift
    
#     idx += 1
#     on = False

def calculate_distance(accel, gps, t=1):
    """
    Calculate the distance traveled using accelerometer and GPS data.

    Args:
        accel (Accel): The accelerometer object.
        gps (GPSModule): The GPS module object.
        t (int): The time step between samples.

    Returns:
        float: The Kalman filtered distance.
    """
    # Initializations
    vel_x = [0,0]
    vel_y = [0,0]
    vel_z = [0,0]
    vel_mag = [0,0]
    distance_accel = 0
    distance_GPS = 0
    prev_gps_position = gps.get_data()
    # Variance values for Kalman Filtering
    sigma = 1
    var_accel = sigma # Accelerometer variance should be increased with time
    var_GPS = sigma

    while True:
        time.sleep(t)

        acc_data = accel.get_corrected_values()  # Get accelerometer data
        acc_x, acc_y, acc_z = acc_data['AcX'], acc_data['AcY'], acc_data['AcZ']

        vel_x[1] = vel_x[0] + (0.5 * t * (acc_x + acc_x))
        vel_y[1] = vel_y[0] + (0.5 * t * (acc_y + acc_y))
        vel_z[1] = vel_z[0] + (0.5 * t * (acc_z + acc_z))

        vel_mag[1] = np.sqrt(vel_x[1]**2 + vel_y[1]**2 + vel_z[1]**2)

        distance_accel += 0.5 * t * (vel_mag[0] + vel_mag[1]) # Distance calculated from accelerometer

        curr_gps_position = gps.get_data()  # Get GPS data
        increment_distance_gps = gps.get_relative_position(prev_gps_position, curr_gps_position) # Calculate the distance traveled between two gps points

        distance_GPS += increment_distance_gps # Distance calculated from GPS
        distance_fused = (var_GPS*distance_accel + var_accel*distance_GPS) / (var_accel + var_GPS) # Kalman filtered distance

        vel_x[0] = vel_x[1]
        vel_y[0] = vel_y[1]
        vel_z[0] = vel_z[1]
        vel_mag[0] = vel_mag[1]

        if var_accel < 100: # to prevent numerical overflow
            var_accel += 1 # to account for drift

        print(distance_fused)
