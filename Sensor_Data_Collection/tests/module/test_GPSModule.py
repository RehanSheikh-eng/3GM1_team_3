from Sensor_Data_Collection.modules.GPSModule import GPSModule
import utime as time

GPS_UART_ID = 1
GPS_UART_BAUD_RATE = 9600
GPS_TX_PIN = 4
GPS_RX_PIN = 5
OUTPUT_FILE_NAME = "gps_data.csv"

def main():
    gps_module = GPSModule(uart_id=GPS_UART_ID,
                    baud_rate=GPS_UART_BAUD_RATE,
                    tx_pin_id=GPS_TX_PIN,
                    rx_pin_id=GPS_RX_PIN
                    )

    data_prev = None

    # Open the file in write mode, 'a' is for append
    with open(OUTPUT_FILE_NAME, 'a') as file:
        # Write the header row
        file.write("timestamp,latitude,longitude,relative_position\n")

        while True:
            data = gps_module.get_data()
            if data is not None:
                # Write a row to the CSV file
                file.write(f"{data['timestamp']},{data['latitude']},{data['longitude']},")
                
                print(f"Timestamp: {data['timestamp']}")
                print(f"Latitude: {data['latitude']}")
                print(f"Longitude: {data['longitude']}")

                if data_prev is not None:
                    distance = gps_module.get_relative_position(data_prev, data)
                    file.write(f"{distance}\n")
                    print(f"Relative position: {distance}")
                else:
                    file.write("\n")

                data_prev = data

            time.sleep(1)  # Sleep for a second to avoid spamming the console

if __name__ == "__main__":
    main()
