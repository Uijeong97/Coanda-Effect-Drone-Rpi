#!/usr/bin/python
"""
Control PWM Motors
"""

from __future__ import division
import time
#import RPi.GPIO as GPIO

class Servo:

    # Initialize motor
    def __init__(self,pin,GPIO):
        self.speed = 0
        self.hz = 50
        self.pin = pin
        self.GPIO = GPIO
        self.GPIO.setup(pin, self.GPIO.OUT)
        self.power = self.GPIO.PWM(pin, self.hz)
        self.power.start(7.3)

    # Set motor speed (increase|decrease|0-100)
    def set_speed(self, speed):
        if speed == "increase":
            new_speed = self.get_speed()+1
        elif speed == "decrease":
            new_speed = self.get_speed()-1
        else:
            new_speed = speed
        if new_speed < 0:
            new_speed = 0
        elif new_speed > 100:
            new_speed = 100
        self.speed = new_speed
        self.power.ChangeDutyCycle(new_speed/10)

    # Get current motor speed
    def get_speed(self):
        return self.speed

    # Start motor
    def start(self, start_dc):
        self.power.start(start_dc)
        #self.set_speed(40)

    # Stop motor
    def stop(self, exit):
        self.set_speed(0)
        self.power.stop()
        if exit == True:
            self.GPIO.cleanup()
    
    def motor_ctrl(self, angle):
        for i in range(3,13):
            desiredPosition=angle
            DC=1./18*(desiredPosition)+7.3 #servo initial position
            self.power.ChangeDutyCycle(DC)
    