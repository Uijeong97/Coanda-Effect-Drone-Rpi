#!/usr/bin/python
# Accelerometer/Gyrometer Sensor - GY-521 (ITG/MPU) / MPU-6050
# Revisions: 1 - Newer, 0 - Older

import smbus, math, time
import RPi.GPIO as GPIO

class Gyro:
    
    def __init__(self,devNum):   #rev = 1 (rpi3B)
        self.pwr_mgmt_1 = 0x6b
        self.pwr_mgmt_2 = 0x6c
        
        self.bus = smbus.SMBus(1)
        self.devN = 68 + devNum
        self.dev_addr = 0x(self.devN)
        
        self.accel_xout = 0x3b
        self.accel_yout = 0x3d
        self.accel_zout = 0x3f
        
        self.gyro_xout = 0x43
        self.gyro_yout = 0x45
        self.gyro_zout = 0x47
        
        self.bus.write_byte_data(self.dev_addr, self.pwr_mgmt_1, 0)

    # 1byte read
    def read_byte(self,adr):
        return self.bus.read_byte_data(self.dev_addr, adr)

    # 2byte read
    def read_word(self,adr):
        high = self.read_byte(self.dev_addr, adr)
        low = self.read_byte(self.dev_addr, adr+1)
        val = (high << 8) + low
        return val

    # Sensor data read
    def read_word_sensor(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
        
#-----------------------------------
    def dist(self,a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self,x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)
    
    def get_z_rotation(x,y,z):
        radians = math.atan2(z, dist(x,y))
        return math.degrees(radians)
#-----------------------------------
    # get gyro data
    def get_gyro_data_lsb():
        x = read_word_sensor(self.accel_xout)
        y = read_word_sensor(self.accel_yout)
        z = read_word_sensor(self.accel_zout)
        return [x, y, z]
    
    def get_gyro_data_deg():
        x,y,z = get_gyro_data_lsb()
        x = x / 131.0
        y = y / 131.0
        z = z / 131.0
        return [x, y, z]
    
    # get accel data
    def get_accel_data_lsb():
        x = read_word_sensor(self.accel_xout)
        y = read_word_sensor(self.accel_yout)
        z = read_word_sensor(self.accel_zout)
        return [x, y, z]
    
    # get accel data
    def get_accel_data_g():
        x,y,z = get_accel_data_lsb()
        x = x / 16384.0
        y = y / 16384.0
        z = z / 16384.0
        return [x, y, z]
