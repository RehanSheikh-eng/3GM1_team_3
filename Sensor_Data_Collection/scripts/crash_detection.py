import math
import time

def crash_detection(accel, distance_sensor, DEBUG=False, time_step=1):
    """
    Crash detection routine using accelerometer, GPS, and distance sensor data.

    Args:
        accel: Accelerometer object.
        distance_sensor: Distance sensor object.
        previous_accel_data: Previous accelerometer data for comparison.
        DEBUG: Debug mode flag. If True, debugging output will be printed.
        time_step: Time step for each iteration in seconds.
    """
    previous_gps_data = None 
    previous_accel_data = None
    jerk = None

    global current_true_crashes  
    current_true_crashes = 0

    while True:
        try:
            # Get accelerometer data
            accel_data = accel.get_corrected_values()

            # Get magnitude of acceleration and angular velocity
            acc_mag = math.sqrt(accel_data["AcX"]**2 + accel_data["AcY"]**2 + accel_data["AcZ"]**2)
            gyro_mag = math.sqrt(gyro_data["Gx"]**2 + gyro_data["Gy"]**2 + gyro_data["Gz"]**2)
            
            # Calculate jerk (rate of change of acceleration)
            
            if previous_accel_data is not None:
                previous_acc_mag = math.sqrt(previous_accel_data["AcX"]**2 + previous_accel_data["AcY"]**2 + previous_accel_data["AcZ"]**2)
                jerk = (acc_mag - previous_acc_mag) / time_step
            

            # Get distance data
            distance = distance_sensor.get_smooth_distance()
                
            # Check if we have a potential crash
            if jerk > 5 and acc_mag > 6 and gps_distance < 0.5 and distance < 100 and gyro_mag > 0.5:
                current_true_crashes += 1
                if DEBUG:
                    print("Crash Detected")

            # Store previous data
            previous_accel_data = accel_data

            # Debugging output
            if DEBUG:
                print(f"Acceleration Magnitude: {acc_mag}ms^-2")
                print(f"Jerk: {jerk if jerk is not None else 'N/A'}ms^-3")
                print(f"Gyro Magnitude: {gyro_mag}°/s")
                print(f"GPS Distance: {gps_distance if previous_gps_data is not None else 'N/A'}m")
                print(f"Distance: {distance}mm")

            time.sleep(time_step)

        except Exception as e:
            print(f"An error occurred during the crash detection routine: {e}")
            continue
