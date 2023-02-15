# Test Folder Files

## Streaming/Ultrasonic Sensor Test

1. These files run on a computer that will act as a server, not the raspberrypi
2. For video streaming/ultrasonic sensor test, start the server program first
3. Start the corresponding client program in the "raspberryPi" folder on the rasperrbypi.

## RC Control Files

There are two ways to manually control the RC Car.

### Orginal Method

The first way is to take the orginal RC Controller and attach wires to ground the inputs via a microcontroller like the Arduino UNO. This method means the Arduino stays connected to the server computer for the manual control data collection.

### H Bridge Control

This implementation uses an H bridge motor driver to control the RC car. Meaning everything except for the battery pack and the motors are gutted from the RC Car. Most budget RC Cars from stores like Target, Ross, and Walmart only have two motors. One motor is attached to the front of the car with an attachment to translate rotational movement into linear movement for left/right steering. The other is usally in the rear of the car which controls forward and reverse movement.

This implementations requires the arduino to be on board the RC Car and will be in a SPI Slave congfiguations with a raspberry pi.

The file `h_bridge_control_server_test.py` will create a socket connection with the client (the rPi).
