import sys
import smbus
import math
import time
from time import sleep
from Gyro import Gyro
 
gyro = Gyro()
   
def originValue() :
    try:
        while True:
                    time.sleep(1)
                    print "--------------------------------------------------------"
                    print "=>init gyro data"
                    print "---------"
                    gyro_xout, gyro_yout, gyro_zout = gyro.get_gyro_data_lsb()
                    print "gyro_xout: ", gyro_xout,"gyro_yout: ", gyro_yout, "gyro_zout: ", gyro_zout
                    print
                    print "=> init accelerometer data"
                    print "------------------"
                    accel_xout, accel_yout, accel_zout = gyro.get_accel_data_lsb()
                    print "accel_xout: ", accel_xout, "accel_yout: ", accel_yout, "accel_zout: ", accel_zout, 
                    print
                    print "Confirm accel_zout is near by 16384 --> then OK" 
                    print "--------------------------------------------------------"
                    print
                    print
                    print "--------------------------------------------------------"

    except KeyboardInterrupt:
         GPIO.cleanup()
 
def calc_average():
   
    num_readings = 10;
    gyro_x = 0
    gyro_y = 0
    gyro_z = 0
    accel_x = 0
    accel_y = 0
    accel_z = 0

    print "Starting Calibration"

    for i in range (num_readings):
        gyro_x += gyro.read_word_sensor(gyro.gyro_xout)
        gyro_y += gyro.read_word_sensor(gyro.gyro_yout)
        gyro_z += gyro.read_word_sensor(gyro.gyro_zout)
        accel_x += gyro.read_word_sensor(gyro.accel_xout)
        accel_y += gyro.read_word_sensor(gyro.accel_yout)
        accel_z += gyro.read_word_sensor(gyro.accel_zout)
        #gyro_xout, gyro_yout, gyro_zout = gyro.get_gyro_data_lsb()
        #accel_xout, accel_yout, accel_zout += gyro.get_accel_data_lsb()
        time.sleep(1)

    gyro_x /= num_readings
    gyro_y /= num_readings 
    gyro_z /= num_readings 
    accel_x /= num_readings 
    accel_y /= num_readings 
    accel_z /= num_readings
    
    # Store the raw calibration values globally

    #base_x_accel = accel_xout
    #base_y_accel = accel_yout 
    #base_z_accel = accel_zout 
    #base_x_gyro = gyro_xout
    #base_y_gyro = gyro_yout
    #base_z_gyro = gyro_zout

    print "Finishing Calibration"
    
    return [gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z]
    #return [base_x_gyro, base_y_gyro, base_z_gyro, base_x_accel, base_y_accel, base_z_accel

def get_gyro_deg(base_gyX, base_gyY, base_gyZ):
    FS_SEL = 131
    #gyX, gyY, gyZ = 0
    gyX = (gyro.read_word_sensor(gyro.gyro_xout) - base_gyX) / FS_SEL
    gyY = (gyro.read_word_sensor(gyro.gyro_yout) - base_gyY) / FS_SEL
    gyZ = (gyro.read_word_sensor(gyro.gyro_zout) - base_gyZ) / FS_SEL
    
    #dt ????
    gyro_angle_x += gyro_x * dt
    gyro_angle_y += gyro_y * dt
    gyro_angle_z += gyro_z * dt
    #dt = (t_now - get_last_time()) / 1000.0
    #gyro_angle_x = gyro_x*dt + get_last_x_angle()
    #gyro_angle_y = gyro_y*dt + get_last_y_angle()
    #gyro_angle_z = gyro_z*dt + get_last_z_angle()
    
    return [gyX, gyY, gyZ]



def get_accel_deg(base_acX, base_acY, base_acZ):
    G_CONVERT = 16384
    #acX, acY, acZ = 0
    acX = gyro.read_word_sensor(gyro.accel_xout) - base_acX
    acY = gyro.read_word_sensor(gyro.accel_xout) - base_acY
    acZ = gyro.read_word_sensor(gyro.accel_xout) - base_acZ

    return [acX, acY, acZ]


base_x_gyro, base_y_gyro, base_z_gyro, base_x_accel, base_y_accel, base_z_accel = calc_average()
print "base_x_gyro : ", base_x_gyro, "base_y_gyro: ", base_y_gyro, "base_x_gyro: ", base_z_gyro
print "base_x_accel : ", base_x_accel, "base_y_accel : ", base_y_accel, "base_z_accel : ", base_z_accel
try:
    while True:
        gyX, gyY, gyZ = get_gyro_deg(base_x_gyro, base_y_gyro, base_z_gyro)
        acX, acY, acZ = get_accel_deg(base_x_accel, base_y_accel, base_z_accel)

        print "gyro_xout: ", gyX,"gyro_yout: ", gyY, "gyro_zout: ", gyZ
        print "accel_xout: ", acX, "accel_yout: ", acY, "accel_zout: ", acZ
        time.sleep(1)
except KeyboardInterrupt:
         GPIO.cleanup()
   
