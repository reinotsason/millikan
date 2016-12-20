import serial


class VoltageController(object):
    """ Class to represent the voltage controller """

    def __init__(self, port='/dev/ttyACM0', rate=115200):
        """ Set up the voltage controller.

        Keyword arguments:
        port -- port that the Arduino is connected to
        rate -- Baud rate for communication
        """

        self.ser = serial.Serial(port=port, baudrate=rate)

    def send_voltage(self, voltage):
        """ Set the voltage on the controller.

        Arguments:
        voltage -- voltage to be set in volts
        """

        text = 'v' + str(voltage)
        data = text.encode(encoding='ascii')
        self.ser.write(data)

    def get_voltage(self):
        """ Get the measured voltage from the monitor port of the controller

        Arguments: None
        """

        data = 'r'.encode(encoding='ascii')
        self.ser.write(data)
        bytes_to_read = self.ser.in_waiting
        voltage_level = self.ser.read(bytes_to_read)

        return voltage_level
