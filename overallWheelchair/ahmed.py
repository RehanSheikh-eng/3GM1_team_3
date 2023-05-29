# --- CRASH PREVENTION ---


from collections import deque
from Sensor_Data_Collection.modules.DistanceSensorModule import DistanceSensor

current_total_crashes = 0

distance_sensor = DistanceSensor(id = DIST_ID, 
                                sda = DIST_SDA_PIN,
                                scl = DIST_SCL_PIN
                                )

# Get 3-order moving average of  distance
distance_sensor = DistanceSensor()
distance_buffer = deque([0,0,0])
distance_buffer.popleft
distance_buffer.append(distance_sensor.get_distance())
distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3

def startCrashPrevention(distance):
    global current_total_crashes

    if distance < 500 and 