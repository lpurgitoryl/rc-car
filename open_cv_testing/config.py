# decided to make a config file bc changing the port and server location gets annoying

# port for serial connection
serial_port = '/dev/ttyACM0'
# mac_port use '/dev/tty.usbmodem1421'

# server location
# If running a VM, Use a NAT bridge config.
# run 'ifconfig' and use the inet addr for the wifi in the form 192.168.1.X
iphone = '172.20.10.3'
home = '192.168.1.28'
andriod = '192.168.116.85'
server_addr = iphone
# iphone '172.20.10.1'

# the ultrasonic sensor and the pi camera run on the same server but diffrent ports
# im too lazy to add them here but you can put them below 