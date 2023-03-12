import serial
import time

arduino = serial.Serial(port='/dev/ttyS7',baudrate=115200, timeout=.1)
# https://stackoverflow.com/questions/45041604/pyserial-code-working-on-windows-com1-but-not-on-linux-dev-ttys0

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


while True:
    num = input("Enter a number: ")
    value = write_read(num)
    print(value)