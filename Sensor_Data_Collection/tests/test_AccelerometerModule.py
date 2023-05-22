from Sensor_Data_Collection.modules.AccelerometerModule import Accel

# Define PINS/CONSTS
ACCEL_SDA_PIN = 8
ACCEL_SCL_PIN = 9

def main():
    accel = Accel(sda_pin=ACCEL_SDA_PIN,
            scl_pin=ACCEL_SCL_PIN
            )

    while True:
        data = accel_module.get_corrected_values()
        
        print(f"Timestamp: {data['timestamp']}")
        print(f"AccX: {data['AcX']}")
        print(f"AccY: {data['AcY']}")
        print(f"AccZ: {data['AcZ']} (corrected for gravity)")
        print(f"GyroX: {data['GyroX']}")
        print(f"GyroY: {data['GyroY']}")
        print(f"GyroZ: {data['GyroZ']}")

        time.sleep(1)  # Sleep for a second to avoid spamming the console

if __name__ == "__main__":
    main()
