#!/usr/bin/python
# Accelerometer/Gyrometer Sensor - GY-521 (ITG/MPU) / MPU-6050
# Revisions: 1 - Newer, 0 - Older

import smbus, math, time
import RPi.GPIO as GPIO
import csv

class Gyro:
    
    def __init__(self):   #rev = 1 (rpi3B)
        self.pwr_mgmt_1 = 0x6b # pwr mamt register address
        self.pwr_mgmt_2 = 0x6c # not use
        
        self.bus = smbus.SMBus(1)
        # self.devN = 68 + devNum
        self.dev_addr = 0x68 # mpu6050 device's i2c basic address
        
        # if you want to know code below, you can see this on MPU-6050 register table
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
        high = self.read_byte(adr)
        low = self.read_byte(adr+1)
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

    def get_x_rotation(self,x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_y_rotation(self,x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)
    
    def get_z_rotation(self,x,y,z):
        radians = math.atan2(z, dist(x,y))
        return math.degrees(radians)
#-----------------------------------
    # get gyro data
    def get_gyro_data_lsb(self):
        x = self.read_word_sensor(self.gyro_xout)
        y = self.read_word_sensor(self.gyro_yout)
        z = self.read_word_sensor(self.gyro_zout)
        return [x, y, z]
    
    # get gyro data
    # FS_SEL register = 0 -> gyro sensor value (1 deg/s = 131)
    def get_gyro_data_deg(self):
        x,y,z = self.get_gyro_data_lsb()
        x = x / 131.0
        y = y / 131.0
        z = z / 131.0
        return [x, y, z]
    
    # get accel data
    def get_accel_data_lsb(self):
        x = self.read_word_sensor(self.accel_xout)
        y = self.read_word_sensor(self.accel_yout)
        z = self.read_word_sensor(self.accel_zout)
        return [x, y, z]
    
    # get accel data
    # AFS_SEL register = 0 -> accel sensor value per g = 16384/g
    def get_accel_data_g(self):
        x,y,z = self.get_accel_data_lsb()
        x = x / 16384.0
        y = y / 16384.0
        z = z / 16384.0
        return [x, y, z]


gyro=Gyro()
f = open('gyro_data.csv', 'w')
wr = csv.writer(f)

try:
    while True:
        gyro_x,gyro_y,gyro_z = gyro.get_gyro_data_deg()
        accel_x,accel_y,accel_z = gyro.get_accel_data_g()
        wr.writerow([gyro_x,gyro_y,gyro_z,accel_x,accel_y,accel_z])
        time.sleep(1)
except:
        GPIO.cleanup()
        f.close()