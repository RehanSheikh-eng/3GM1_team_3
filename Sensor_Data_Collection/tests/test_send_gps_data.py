from Sensor_Data_Collection.modules.GPSModule import GPSModule
from Sensor_Data_Collection.modules.L2S2Module import L2S2Module
import utime as time

GPS_UART_ID = 1
GPS_UART_BAUD_RATE = 9600
GPS_TX_PIN = 4
GPS_RX_PIN = 5

def main():
    gps_module = GPSModule(uart_id=GPS_UART_ID,
                    baud_rate=GPS_UART_BAUD_RATE,
                    tx_pin_id=GPS_TX_PIN,
                    rx_pin_id=GPS_RX_PIN
                    )

    l2s2_module = L2S2Module("AndroidAP", "wtdm1984")
    data_prev = None

    while True:
        data = gps_module.get_data()
        if data is not None:
            print(f"Timestamp: {data['timestamp']}")
            print(f"Latitude: {data['latitude']}")
            print(f"Longitude: {data['longitude']}")
            l2s2_module.send_data("110", "6e0485b5-cd17-4438-aff8-afe0578ed71f", "4", type = 5, content = data["longitude"], units = "degrees")

            if data_prev is not None:
                distance = gps_module.get_relative_position(data_prev, data)
                print(f"Relative position in meters: {distance}")

            data_prev = data

        time.sleep(1)  # Sleep for a second to avoid spamming the console

if __name__ == "__main__":
    main()
