#import os, time

#os.system ("sudo pigpiod") #Launching GPIO library
#time.sleep(1) 

#import pigpio
import sys
import smbus
import math
import time
from time import sleep  # time module
import RPi.GPIO as GPIO
from Servo import Servo
from esc_class import bldc_motor

GPIO.setmode(GPIO.BCM)

motor = bldc_motor(4, 2000, 800, 1000)
servo_1 = Servo(18, GPIO)
servo_2 = Servo(17, GPIO)
print "For first time launch, enter calibrate"
print "else, skip"

inp = raw_input()
if inp == "calibrate":
    motor.calibrate()
else :
    print "program start"

print 'Waiting for commands...'

print '<--------command content-------->'
print '[bldc ctrl]   |   [servo ctrl]'
print '     k        |         w'
print '     l        |       a s d'
print 'k,l: fast, slow'
print 'w,s: front, rear'
print 'a,d: left, right\n\n'

try:
    while True:
        
        command = raw_input('Enter command: ')
    
        if command == 'k':
            motor.keyUp()
        elif command == 'l':
            motor.keyDown()
        
        elif command == 'w':
            servo_1.set_speed('increase')
        elif command == 's':
            servo_1.set_speed('decrease')
            
        elif command == 'a':
            servo_2.set_speed('increase')
           
        elif command == 'd':
            servo_2.set_speed('decrease')

        elif command == 'stop':
            servo_1.stop()
            servo_2.stop()
            motor.stop()
        
            
except KeyboardInterrupt:
    print '== servo stop =='

servo_1.stop()
servo_2.stop()
motor.stop()