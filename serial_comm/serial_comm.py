import serial


class VoltageController(object):
    """ Class to represent the voltage controller """

    def __init__(self, port='/dev/ttyACM0', rate=115200,
                 write_max_scale=975, write_min_scale=3,
                 read_max_scale=950, read_min_scale=0):
        """ Set up the voltage controller.

        Keyword arguments:
        port -- port that the Arduino is connected to
        rate -- Baud rate for communication
        """

        self.ser = serial.Serial(port=port, baudrate=rate)
        self.write_max_scale = write_max_scale
        self.write_min_scale = write_min_scale
        self.read_max_scale = read_max_scale
        self.read_min_scale = read_min_scale


    def send_voltage(self, voltage):
        """ Set the voltage on the controller.

        Arguments:
        voltage -- voltage to be set in volts
        """

        voltage_level = (voltage - self.write_min_scale) / (self.write_max_scale - self.write_min_scale)
        voltage_level = int(voltage_level)

        if voltage_level > 4095:
            voltage_level = 4095
        elif voltage_level < 0:
            voltage_level = 0

        text = 'v' + str(voltage_level)
        data = text.encode(encoding='ascii')
        self.ser.write(data)

    def get_voltage(self):
        """ Get the measured voltage from the monitor port of the controller

        Arguments: None
        """

        data = 'r'.encode(encoding='ascii')
        self.ser.write(data)
        bytes_to_read = self.ser.in_waiting
        voltage_level = int(self.ser.read(bytes_to_read))

        voltage = self.read_min_scale + (voltage_level / 4095) * (self.read_max_scale - self.read_min_scale)

        return voltage
