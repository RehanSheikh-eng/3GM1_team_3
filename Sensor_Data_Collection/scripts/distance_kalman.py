import math

class KalmanFilter1D:
    def __init__(self, R_acc, R_gps, Q):
        self.x = 0  # initial state (distance)
        self.P = 1000  # initial uncertainty
        self.R_acc = R_acc  # measurement noise for accelerometer
        self.R_gps = R_gps  # measurement noise for GPS
        self.Q = Q  # process noise

    def predict(self):
        return self.x

    def update_acc(self, acc_distance):
        # Update state
        self.x += acc_distance
        # Update uncertainty
        self.P += self.Q
        # Debug
        print('update_acc: x={}, P={}'.format(self.x, self.P))

    def update_gps(self, gps_distance):
        # Kalman gain
        K = self.P / (self.P + self.R_gps)
        # Update state
        self.x += K * (gps_distance - self.x)
        # Update uncertainty
        self.P = (1 - K) * self.P
        # Debug
        print('update_gps: x={}, P={}, K={}'.format(self.x, self.P, K))



class Fusion:

    def __init__(self, accel, gps, R_acc, R_gps, Q, init_buffer=10):
        self.accel = accel
        self.gps = gps
        self.kf = KalmanFilter1D(R_acc, R_gps, Q)
        self.prev_gps_data = None
        self.prev_timestamp = 0
        self.init_buffer = init_buffer  # add initialization buffer
        self.buffer_count = 0  # initialize buffer count

    def calculate_distance(self, current_timestamp, gps_data):
        # Get accelerometer data and calculate distance
        accel_data = self.accel.get_corrected_values()
        print("Accelerometer readings: ", accel_data)
        dt = (current_timestamp - self.prev_timestamp) / 1000  # time delta in seconds
        
        
        # Check buffer count
        if self.buffer_count < self.init_buffer:
            self.buffer_count += 1
            acc_distance = 0  # ignore initial readings
        else:
            acc_distance = self.calculate_accel_distance(accel_data, dt)

        # Update the filter with accelerometer data
        self.kf.update_acc(acc_distance)

        # Update GPS data only if it's not None
        if gps_data is not None:
            if self.prev_gps_data is not None:
                gps_distance = self.gps.get_relative_position(self.prev_gps_data, gps_data)
                # Update the filter with GPS data
                self.kf.update_gps(gps_distance)
            self.prev_gps_data = gps_data
        # Get the current state estimate
        distance = self.kf.predict()

        self.prev_timestamp = current_timestamp

        return distance


    @staticmethod
    def calculate_accel_distance(accel_data, dt):
        # Here you'll use the accelerometer data to calculate the distance travelled.
        # You might need to integrate twice if you're going from acceleration to distance.
        # Assuming accel_data is a vector containing [accel_x, accel_y, accel_z].
        accel_mag = math.sqrt(accel_data.AccX**2 + accel_data.AccY**2 + accel_data.AccZ**2)
        distance = 0.5 * accel_mag * dt**2
        return distance



