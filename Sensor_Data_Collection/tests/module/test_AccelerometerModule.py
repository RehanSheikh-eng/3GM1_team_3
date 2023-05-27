from Sensor_Data_Collection.modules.AccelerometerModule import Accel
import utime as time

# Define PINS/CONSTS
ACCEL_SDA_PIN = 0
ACCEL_SCL_PIN = 1
ACCEL_I2C_ID = 0
OUTPUT_FILE_NAME = "accel_data.csv"

def main():
    accel = Accel(i2c_id=0,
            sda_pin=ACCEL_SDA_PIN,
            scl_pin=ACCEL_SCL_PIN
            )

    # Open the file in write mode, 'a' is for append
    with open(OUTPUT_FILE_NAME, 'a') as file:
        # Write the header row
        file.write("timestamp,AccX,AccY,AccZ,GyroX,GyroY,GyroZ\n")

        while True:
            data = accel.get_corrected_values()
            #print(f"Timestamp: {data['timestamp']}")
            print(f"AccX: {data.AccX}")
            print(f"AccY: {data.AccY}")
            print(f"AccZ: {data.AccZ} (corrected for gravity)")
            print(f"GyroX: {data.GyroX}")
            print(f"GyroY: {data.GyroY}")
            print(f"GyroZ: {data.GyroZ}")

            # Write a row to the CSV file
            file.write(f"{time.time()},{data.AccX},{data.AccY},{data.AccZ},{data.GyroX},{data.GyroY},{data.GyroZ}\n")

            time.sleep_ms(100)  # Sleep for a second to avoid spamming the console

if __name__ == "__main__":
    main()

