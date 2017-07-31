import serial
import serial.tools.list_ports

arduino_serial_number = '75237333536351F0F0C1'

# server_address_home = ('192.168.0.88', 45713)
server_address_corp = ('10.72.76.108', 45713)
server_address = server_address_corp

rpi = "10.104.66.208', 49214"

def find_arduino(serial_number):
    for p in serial.tools.list_ports.comports():
        if p.serial_number == serial_number:
            return serial.Serial(p.device)

    raise IOError("Could not find the Arduino - is it plugged in!")