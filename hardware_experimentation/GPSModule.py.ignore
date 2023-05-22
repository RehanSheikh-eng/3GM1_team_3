from machine import UART
import ujson as json
import utime as time

class GPSModule:
    """
    A class used to represent an gy-gps6mv2 GPS Module.
    
    The class allows for the initialization and control of the GPS module, 
    including the ability to retrieve and parse GPS data from the module.

    Attributes
    ----------
    uart : UART
        The UART object that represents the UART communication interface.

    Methods
    -------
    __init__(uart_id=1, baud_rate=9600):
        Initializes the GPSModule object.
    get_data():
        Gets the data from the GPS module.
    parse_gpgga_string(gpgga_string):
        Parses a GPGGA string to extract the GPS data.
    dump_to_json(filepath):
        Dumps the GPS data to a JSON file.
    """
    def __init__(self, uart_id=1, baud_rate=9600):
        """
        Initializes the GPSModule object.

        Args:
            uart_id (int): The UART identifier which the GPS module is connected.
            baud_rate (int): The baud rate for serial communication.
        """
        self.uart = UART(uart_id, baud_rate)
        self.uart.init(baud_rate, bits=8, parity=None, stop=1)

    def get_data(self):
        """
        Gets the data from the GPS module.

        Returns:
            dict: A dictionary containing the timestamp, latitude, and longitude.
        """
        if self.uart.any():
            line = self.uart.readline()
            if line:
                data = self.parse_gpgga_string(line)
                return data

    def parse_gpgga_string(self, gpgga_string):
        """
        Parses a GPGGA string to extract the GPS data.

        Args:
            gpgga_string (str): The GPGGA string to parse.

        Returns:
            dict: A dictionary containing the timestamp, latitude, and longitude.
        """
        components = gpgga_string.decode().split(",")
        if "$GPGGA" in components[0]:
            timestamp = components[1]
            latitude = components[2]
            longitude = components[4]
            return {
                "timestamp": timestamp,
                "latitude": latitude,
                "longitude": longitude
            }
        else:
            return None

    def dump_to_json(self, filepath):
        """
        Dumps the GPS data to a JSON file.

        Args:
            filepath (str): The path to the JSON file.
        """
        data = self.get_data()
        if data:
            with open(filepath, 'w') as f:
                json.dump(data, f)

    def convert_to_degrees(raw_value):
        """
        Converts longitude to degree format

        Args:
            raw_value : Raw longitude/latitude value
        """
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position


    def get_relative_position(self, gpgga1, gpgga2):
        """
        Calculates the difference in position between two GPGGA strings.

        Args:
            gpgga1 (str): The first GPGGA string.
            gpgga2 (str): The second GPGGA string.

        Returns:
            float: The difference in position in meters.
        """
        pos1 = self.parse_gpgga_string(gpgga1)
        pos2 = self.parse_gpgga_string(gpgga2)

        lat1 = self.convert_to_degrees(float(pos1['latitude']))
        lon1 = self.convert_to_degrees(float(pos1['longitude']))
        lat2 = self.convert_to_degrees(float(pos2['latitude']))
        lon2 = self.convert_to_degrees(float(pos2['longitude']))

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Approximate radius of earth in km
        R = 6371.0

        # Distance
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c * 1000  # convert to meters

        return distance