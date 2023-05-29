def crash_detection_isr(timer):
    accel_data = sensor_data["accel"]
    distance = sensor_data["distance"]
    if accel_data is not None and distance is not None:
        acc_mag = math.sqrt(accel_data.AccX**2 + accel_data.AccY**2)
        jerk = None
        if previous_data["accel"] is not None:
            prev_acc_mag = math.sqrt(previous_data["accel"].AccX**2 + previous_data["accel"].AccY**2 )
            jerk = (acc_mag - prev_acc_mag) / (time_crash_detection/1000) # Assuming this ISR runs every 1s
        # Update previous data
        previous_data["accel"] = accel_data

        if jerk > 50 and acc_mag > 6 and distance < 100:  # Add gyro condition if needed
            current_true_crashes += 1
            if DEBUG:
                print("Crash Detected")