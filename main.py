import sys
import smbus
import math
import time
from time import sleep  # time module
import RPi.GPIO as GPIO
from Servo import Servo
from Gyro import Gyro

# ---------------------------------------

# ---------------------------------------

GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)


print 'Initializing sensors and misc boards...'

gyro = Gyro()
# gps = GPS() # 모듈 시킨거 안왔습니당



print 'Initializing motors...'

servo_1 = Servo(18, GPIO)
servo_2 = Servo(17, GPIO)


print 'Waiting for commands...'

while True:
	command = raw_input('Enter command: ')

	if command == 'increase front':
		front_left.set_speed('increase')
		front_right.set_speed('increase')

	elif command == 'increase back':
		rear_left.set_speed('increase')
		rear_right.set_speed('increase')

	elif command == 'speed 50':
		front_left.set_speed(50)
		front_right.set_speed(50)
		rear_left.set_speed(50)
		rear_right.set_speed(0)
