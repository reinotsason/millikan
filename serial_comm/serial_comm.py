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

        data = str(voltage).encode(encoding='ascii')
        self.ser.write(data)
