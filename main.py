import sys
import smbus
import math
import time
from time import sleep  # time module
import RPi.GPIO as GPIO
from Servo import Servo
from Gyro import Gyro
from esc_class import bldc_motor

# ---------------------------------------

# ---------------------------------------

GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)


print 'Initializing sensors and misc boards...'

gyro = Gyro()
# gps = GPS() # 모듈 시킨거 안 왔음


print 'Initializing servo motors...'

servo_1 = Servo(18, GPIO)
servo_2 = Servo(17, GPIO)
# servo_3 = Servo(17, GPIO)
# servo_4 = Servo(17, GPIO)
# servo_5 = Servo(17, GPIO)
# servo_6 = Servo(17, GPIO)

motor = bldc_motor(4, 2000, 700, 800)

print 'Waiting for commands...'

print '<--------command content-------->'
print '[bldc ctrl]   |   [servo ctrl]'
print '     k        |         w'
print '     l        |       a s d'
print 'k,l: fast, slow'
print 'w,s: front, rear'
print 'a,d: left, right'

try:
	while True:
		accel_x,accel_y,accel_z = gyro.get_accel_data_g()
        	x_angle = gyro.get_x_rotation(accel_x, accel_y, accel_z)
        	y_angle = gyro.get_y_rotation(accel_x, accel_y, accel_z)
        
        	servo_1.motor_ctrl(x_angle)
        	servo_2.motor_ctrl(y_angle)
		
		command = raw_input('Enter command: ')
	
		if command == 'k':
			motor.keyUp()
		elif command == 'l':
			motor.keyDown()
		
		elif command == 'w':
			servo_1.set_speed('increase')
			time.sleep(1)
		elif command == 's':
			servo_1.set_speed('decrease')
			time.sleep(1)
		elif command == 'a':
			servo_2.set_speed('increase')
			time.sleep(1)
		elif command == 'd':
			servo_2.set_speed('decrease')
			time.sleep(1)

except KeyboardInterrup:
	print '== servo stop =='

servo_1.stop()
servo_2.stop()
motor.stop()
