import numpy as np
import time
import json
import accelerometer
import GPSModule

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
    prev_acc_data = accel.get_corrected_values()

    # Variance values for Kalman Filtering
    sigma = 1 # SET THRESHOLD THORUGH TESTING
    var_accel = sigma # Accelerometer variance should be increased with time
    var_GPS = sigma

    while True:
        time.sleep(t)

        acc_data = accel.get_corrected_values()  # Get accelerometer data IMPLEMENT THIS 

        prev_acc_x, prev_acc_y, prev_acc_z = prev_acc_data['AcX'], prev_acc_data['AcY'], prev_acc_data['AcZ']
        acc_x, acc_y, acc_z = acc_data['AcX'], acc_data['AcY'], acc_data['AcZ']

        # Integrating the acceleromater data
        vel_x[1] = vel_x[0] + (0.5 * t * (prev_acc_x + acc_x))
        vel_y[1] = vel_y[0] + (0.5 * t * (prev_acc_y + acc_y))
        vel_z[1] = vel_z[0] + (0.5 * t * (prev_acc_z + acc_z))

        vel_mag[1] = np.sqrt(vel_x[1]**2 + vel_y[1]**2 + vel_z[1]**2)

        distance_accel += 0.5 * t * (vel_mag[0] + vel_mag[1]) # Distance calculated from accelerometer

        curr_gps_position = gps.get_data()  # Get GPS data
        increment_distance_gps = gps.get_relative_position(prev_gps_position, curr_gps_position) # Calculate the distance traveled between two gps points
        
        distance_GPS += increment_distance_gps # Distance calculated from GPS
        distance_fused = (var_GPS*distance_accel + var_accel*distance_GPS) / (var_accel + var_GPS) # Kalman filtered distance

        # Shift data timestep
        prev_acc_data = acc_data
        vel_mag[0] = vel_mag[1]
        prev_gps_position = curr_gps_position


        if var_accel < 100: # to prevent numerical overflow
            var_accel += 1 # to account for drift

        if vel_mag[0] < 0.001: # SET THRESHOLD THROUGH TESTING
            var_accel = sigma # variance resets when wheelchair is stationary

        return distance_fused
