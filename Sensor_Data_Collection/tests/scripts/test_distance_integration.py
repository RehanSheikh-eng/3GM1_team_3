import utime as time
from Sensor_Data_Collection.modules.GPSModule import GPSModule
from Sensor_Data_Collection.modules.AccelerometerModule import Accel
from Sensor_Data_Collection.scripts.distance_integration_copy import calculate_distance

import collections


GRAVITY_ACCEL = 9.81
class AccelData(
    collections.namedtuple(
        "AccelData", ["AccX", "AccY", "AccZ"]
    )
):
    pass



def test_distance_integration(accel, gps, time_step=1, debug=True):
    """
    Tests the distance calculation function using accelerometer and GPS data.
    It prints the calculated distances and writes the output to a CSV file.

    Args:
        accel (Accel): The accelerometer object.
        gps (GPSModule): The GPS module object.
        time_step (int): The time step between samples.
        debug (bool): Whether to print debug info.
    """

    # Initializations
    prev_gps_position = gps.get_data()
    prev_accel_data = accel.get_corrected_values()
    prev_vel_mag = 0
    var_accel = 1  # variance for accelerometer
    var_GPS = 1  # variance for GPS
    sigma = 1  # standard deviation

    # Open the CSV file for writing
    with open('distance_data.csv', 'w') as file:
        file.write("GPS Distance,Accelerometer Distance,Fused Distance\n")

        start_time = time.time()
        accel_data_samples = []
        gps_data = None
        while time.time() - start_time < 60:  # run for 60 seconds
            accel_data = accel.get_corrected_values()  # Get accelerometer data

            # Correct the acceleration in z-direction by subtracting gravity
            accel_data_samples.append(accel_data)

            # If 100 samples collected, average the data
            if len(accel_data_samples) == 100:
                accel_data = average_accel_data(accel_data_samples)
                accel_data_samples = []  # Reset the samples

                # Get GPS data and calculate distances
                gps_data = gps.get_data()  # Get GPS data

                if debug:
                    print(f"GPS data: {gps_data}")
                    print(f"Accelerometer data: {accel_data}")
                 

            result = calculate_distance(accel, gps, accel_data, gps_data, prev_gps_position, prev_vel_mag, prev_accel_data, var_accel, var_GPS, sigma, time_step)

            if debug:
                print(f"Calculated distances: GPS - {result['distance_GPS']}, Accel - {result['distance_accel']}, Fused - {result['distance_fused']}")
            
            # Write the calculated distances directly to the file
            file.write(f"{result['distance_GPS']},{result['distance_accel']},{result['distance_fused']}\n")

            # Update states for next calculation
            prev_gps_position = result['prev_gps_position']
            prev_vel_mag = result['prev_vel_mag']
            prev_accel_data = result['prev_accel_data']
            var_accel = result['var_accel']
            var_GPS = result['var_GPS']
            
            time.sleep_ms(time_step)

def average_accel_data(samples):
    """
    Calculate the average accelerometer data from a list of samples.

    Args:
        samples (list): The list of accelerometer samples.

    Returns:
        AccelData: The averaged accelerometer data.
    """

    # Initialize counters for each axis
    counter_x = 0
    counter_y = 0
    counter_z = 0

    # Iterate over the samples and accumulate the data
    for sample in samples:
        counter_x += sample.AccX
        counter_y += sample.AccY
        counter_z += sample.AccZ

    # Calculate the averages
    avg_x = counter_x / len(samples)
    avg_y = counter_y / len(samples)
    avg_z = counter_z / len(samples)

    # Return the average data
    return AccelData(avg_x, avg_y, avg_z)

if __name__ == "__main__":
    # Define PINS/CONSTS
    ACCEL_SDA_PIN = 0
    ACCEL_SCL_PIN = 1
    ACCEL_I2C_ID = 0

    GPS_UART_ID = 1
    GPS_UART_BAUD_RATE = 9600
    GPS_TX_PIN = 4
    GPS_RX_PIN = 5
    time_step = 10
    accel = Accel(i2c_id=ACCEL_I2C_ID,
                sda_pin=ACCEL_SDA_PIN,
                scl_pin=ACCEL_SCL_PIN
                )

    gps = GPSModule(uart_id=GPS_UART_ID,
                    baud_rate=GPS_UART_BAUD_RATE,
                    tx_pin_id=GPS_TX_PIN,
                    rx_pin_id=GPS_RX_PIN
                    )
    test_distance_integration(accel, gps, time_step=time_step, debug=True)

