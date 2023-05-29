from Sensor_Data_Collection.modules.DistanceSensorModule import DistanceSensor

DIST_ID = 0
DIST_SDA_PIN = 0
DIST_SCL_PIN = 1
DIST_MA_ORDER = 3

def main():
    distance_sensor = DistanceSensor(id = DIST_ID, 
                                    sda = DIST_SDA_PIN,
                                    scl = DIST_SCL_PIN
                                    )

    while True:
        distance = distance_sensor.get_distance()
        smooth_distance = distance_sensor.get_smooth_distance()

        print(f"Raw distance: {distance} mm")
        print(f"Smooth distance: {smooth_distance} mm")

        time.sleep(1)  # Sleep for a second to avoid flooding the console

if __name__ == "__main__":
    main()
