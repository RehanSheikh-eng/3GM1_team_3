from Sensor_Data_Collection.scripts.distance_kalman import Fusion
from Sensor_Data_Collection.modules.AccelerometerModule import Accel
from Sensor_Data_Collection.modules.GPSModule import GPSModule
import utime as time

# Define PINS/CONSTS
ACCEL_SDA_PIN = 0
ACCEL_SCL_PIN = 1
ACCEL_I2C_ID = 0

GPS_UART_ID = 1
GPS_UART_BAUD_RATE = 9600
GPS_TX_PIN = 4
GPS_RX_PIN = 5
time_step = 10

# Noise parameters for the Kalman filter
R_acc = 10
R_gps = 5
Q = 1

accel = Accel(i2c_id=ACCEL_I2C_ID,
            sda_pin=ACCEL_SDA_PIN,
            scl_pin=ACCEL_SCL_PIN
            )

gps = GPSModule(uart_id=GPS_UART_ID,
                baud_rate=GPS_UART_BAUD_RATE,
                tx_pin_id=GPS_TX_PIN,
                rx_pin_id=GPS_RX_PIN
                )

fusion = Fusion(accel, gps, R_acc, R_gps, Q)

last_print_time = time.ticks_ms()  # Initialize the last print time
last_gps_time = time.ticks_ms()  # Initialize the last GPS data retrieval time

# Open the file to write data
with open('distance_data.csv', 'w') as f:
    f.write('Time,Estimated Distance\n')  # Write the header line

    # Loop for data collection
    while True:
        current_timestamp = time.ticks_ms()
        gps_data = None

        # Only retrieve GPS data if at least 1 second (1000 ms) has passed
        if time.ticks_diff(current_timestamp, last_gps_time) >= 1000:
            gps_data = gps.get_data()
            last_gps_time = current_timestamp

        # Only calculate distance and print if GPS data is not None
        if gps_data is not None:
            distance = fusion.calculate_distance(current_timestamp, gps_data)

            # Only print and write to file if at least 1 second (1000 ms) has passed
            if time.ticks_diff(current_timestamp, last_print_time) >= 1000:
                print("Estimated Distance: ", distance)
                f.write('{},{}\n'.format(current_timestamp, distance))  # Write data to file
                last_print_time = current_timestamp

        time.sleep_ms(time_step)  # Pause for 10 milliseconds
