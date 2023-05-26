import math
import time

def crash_detection(accel, gps, distance_sensor, current_true_crashes, DEBUG=False, time_step=1):
    """
    Crash detection routine using accelerometer, GPS, and distance sensor data.

    Args:
        accel: Accelerometer object.
        gps: GPS object.
        distance_sensor: Distance sensor object.
        previous_gps_data: Previous GPS data for comparison.
        previous_accel_data: Previous accelerometer data for comparison.
        DEBUG: Debug mode flag. If True, debugging output will be printed.
        time_step: Time step for each iteration in seconds.
    """
    previous_gps_data = None 
    previous_accel_data = None
    jerk = None

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
            
            # Get GPS data
            gps_data = gps.get_data()

            # Get distance data
            distance = distance_sensor.get_smooth_distance()

            # If we have previous data to compare to
            if previous_gps_data is not None and jerk is not None:
                # Get distance between current and previous GPS points
                gps_distance = gps.get_relative_position(previous_gps_data, gps_data)
                
                # Check if we have a potential crash
                if jerk > 5 and acc_mag > 6 and gps_distance < 0.5 and distance < 100 and gyro_mag > 0.5:
                    # TRIGGER CRASH DETECTION PROTOCOL:
                    # 1. TRIGGER BUZZER
                    current_true_crashes += 1
                    if DEBUG:
                        print("Crash Detected")

            # Store previous data
            previous_gps_data = gps_data
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
