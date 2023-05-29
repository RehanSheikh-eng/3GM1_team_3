import math
import utime as time

GRAVITY_ACCEL = 9.81  # m/s^2

def calculate_distance(accel, gps, accel_data, gps_data, prev_gps_position, prev_vel_mag, prev_accel_data, var_accel, var_GPS, sigma, time_step):
    """
    Calculate the distance traveled using accelerometer and GPS data.

    Args:
        accel_data (dict): The accelerometer data.
        gps_data (dict): The GPS data.
        prev_gps_position (dict): The previous GPS data.
        prev_vel_mag (float): The previous velocity magnitude.
        prev_accel_data (dict): The previous accelerometer data.
        var_accel (float): The variance of accelerometer.
        var_GPS (float): The variance of GPS.
        sigma (float): The standard deviation.

    Returns:
        dict: The calculated distances and updated states.
    """

    # Initializations
    vel_x = [0, 0]
    vel_y = [0, 0]
    vel_z = [0, 0]
    vel_mag = [prev_vel_mag, 0]
    distance_accel = 0
    distance_GPS = 0
    distance_fused = 0

    # Scaling accelerometer data by gravity
    prev_acc_x, prev_acc_y, prev_acc_z = prev_accel_data.AccX*GRAVITY_ACCEL, prev_accel_data.AccY*GRAVITY_ACCEL, prev_accel_data.AccZ*GRAVITY_ACCEL
    acc_x, acc_y, acc_z = accel_data.AccX*GRAVITY_ACCEL, accel_data.AccY*GRAVITY_ACCEL, accel_data.AccZ*GRAVITY_ACCEL
    
    # Correct the acceleration in z-direction by subtracting gravity
    acc_z -= GRAVITY_ACCEL
    
    # Integrating the accelerometer data
    vel_x[1] = vel_x[0] + (0.5 * (time_step//1000) * (prev_acc_x + acc_x))
    vel_y[1] = vel_y[0] + (0.5 * (time_step//1000) * (prev_acc_y + acc_y))
    vel_z[1] = vel_z[0] + (0.5 * (time_step//1000) * (prev_acc_z + acc_z))

    vel_mag[1] = math.sqrt(vel_x[1]**2 + vel_y[1]**2 + vel_z[1]**2)

    distance_accel += 0.5 * time_step * (vel_mag[0] + vel_mag[1]) # Distance calculated from accelerometer

    # Only update GPS related calculations if new GPS data is available
    if gps_data is not None:
        increment_distance_gps = gps.get_relative_position(prev_gps_position, gps_data) # Calculate the distance traveled between two gps points
        distance_GPS += increment_distance_gps # Distance calculated from GPS
        distance_fused = (var_GPS*distance_accel + var_accel*distance_GPS) / (var_accel + var_GPS) # Kalman filtered distance
        prev_gps_position = gps_data

    if var_accel < 100: # to prevent numerical overflow
        var_accel += 1 # to account for drift

    if vel_mag[0] < 0.001: # SET THRESHOLD THROUGH TESTING
        var_accel = sigma # variance resets when wheelchair is stationary

    return {
        'distance_GPS': distance_GPS,
        'distance_accel': distance_accel,
        'distance_fused': distance_fused,
        'prev_gps_position': prev_gps_position,
        'prev_vel_mag': vel_mag[1],
        'prev_accel_data': accel_data,
        'var_accel': var_accel,
        'var_GPS': var_GPS,
    }

