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
