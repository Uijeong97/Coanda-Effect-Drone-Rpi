import sys
import smbus
import math
import time
from time import sleep
from Gyro import Gyro
 
gyro = Gyro()
   
dt = 0
#gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = 0 # origin value from sensor
base_x_accel, base_y_accel, base_z_accel, base_x_gyro, base_y_gyro, base_z_gyro = 0 # average value 
gyX, gyY, gyZ, acX, acY, acZ = 0 # modified value ( origin - average value )
accel_angel_x, accel_angel_y, accel_angel_z = 0 # accel angel
gyro_angel_x, gyro_angel_y, gyro_angel_z = 0 # gyro angle
filtered_angel_x, filtered_angel_y, filtered_angel_z = 0 # after filter

def origin_value() :
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
 
def celibrate_gyro():
   
    num_readings = 10;
    #gyro_x = 0
    #gyro_y = 0
    #gyro_z = 0
    #accel_x = 0
    #accel_y = 0
    #accel_z = 0

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

    base_x_accel = accel_xout
    base_y_accel = accel_yout 
    base_z_accel = accel_zout 
    base_x_gyro = gyro_xout
    base_y_gyro = gyro_yout
    base_z_gyro = gyro_zout

    print "Finishing Calibration"
    
    #return [gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z]
    #return [base_x_gyro, base_y_gyro, base_z_gyro, base_x_accel, base_y_accel, base_z_accel

def get_gyro_deg(base_gyX, base_gyY, base_gyZ):
    FS_SEL = 131
   
    gyX = (gyro.read_word_sensor(gyro.gyro_xout) - base_gyX) / FS_SEL
    gyY = (gyro.read_word_sensor(gyro.gyro_yout) - base_gyY) / FS_SEL
    gyZ = (gyro.read_word_sensor(gyro.gyro_zout) - base_gyZ) / FS_SEL

    dt = 0.01 #Sample Time 10ms
    gyro_angle_x += gyro_x * dt
    gyro_angle_y += gyro_y * dt
    gyro_angle_z += gyro_z * dt
    #dt = (t_now - get_last_time()) / 1000.0
    #gyro_angle_x = gyro_x*dt + get_last_x_angle()
    #gyro_angle_y = gyro_y*dt + get_last_y_angle()
    #gyro_angle_z = gyro_z*dt + get_last_z_angle()

    #return [gyro_angle_x, gyro_angle_y, gyro_angle_z]



def get_accel_deg(base_acX, base_acY, base_acZ):
    G_CONVERT = 16384
    RACIANS_TO_DGREES = 180 % 3.14159
    
    acX = gyro.read_word_sensor(gyro.accel_xout) - base_acX
    acY = gyro.read_word_sensor(gyro.accel_xout) - base_acY
    acZ = gyro.read_word_sensor(gyro.accel_xout) - base_acZ
    #acZ = gyro.read_word_sensor(gyro.accel_xout) + G_CONVERT - base_acZ

    #require +X = head of drone, +Y wing of drone
    accel_yz = math.sqrt((acY*acY)+(acZ*acZ)) # based on +X
    accel_angel_y = math.atan2(-acX, accel_yz) * RACIANS_TO_DGREES # angle of ROLL

    accel_xz = math.sqrt((acX*acX)+(acZ*acZ)) # based on +Y
    accel_angel_x = math.atan2(acY, accel_xz) * RACIANS_TO_DGREES # angle of PITCH

    accel_angel_z = 0
    #return [accel_angle_x, accel_angle_y, accel_angle_z]

def calcFilteredYPR():
    ALPHA = 0.96
    tmp_angle_x, tmp_angle_y, tmp_angle_z = 0

    tmp_angle_x = filtered_angel_x + gyX * dt
    tmp_angle_y = filtered_angel_y + gyY * dt
    tmp_angle_z = filtered_angel_z + gyZ * dt

    filtered_angel_x = ALPHA * tmp_angle_x + (1.0 - ALPHA) * accel_angle_x
    filtered_angel_y = ALPHA * tmp_angle_y + (1.0 - ALPHA) * accel_angle_y
    filtered_angel_z = tmp_angle_z


try:
    #base_x_gyro, base_y_gyro, base_z_gyro, base_x_accel, base_y_accel, base_z_accel =celibrate_gyro()
    celibrate_gyro()
    print "base_x_gyro : ", base_x_gyro, "base_y_gyro: ", base_y_gyro, "base_x_gyro: ", base_z_gyro
    print "base_x_accel : ", base_x_accel, "base_y_accel : ", base_y_accel, "base_z_accel : ", base_z_accel
    while true:
        #gyX, gyY, gyZ = get_gyro_deg(base_x_gyro, base_y_gyro, base_z_gyro)
        #acX, acY, acZ = get_accel_deg(base_x_accel, base_y_accel, base_z_accel)
        get_gyro_deg(base_x_gyro, base_y_gyro, base_z_gyro)
        get_accel_deg(base_x_accel, base_y_accel, base_z_accel)
        calcFilteredYPR()

        #print "gyro_xout: ", gyX,"gyro_yout: ", gyY, "gyro_zout: ", gyZ
        #print "accel_xout: ", acX, "accel_yout: ", acY, "accel_zout: ", acZ
        print "---------------------------------------------------------------"
        print "                  < init data (modified) >"
        print "gyro  --> x : ", gyX, " y : ", gyY, " z : ", gyZ
        print "accel --> x : ", acX, " y : ", acY, " z : ", acZ
        print 
        print "                        < angel >"
        print "gyro  --> x : ", gyro_angel_x, " y : ", gyro_angel_y, " z : ", gyro_angel_z
        print "accel --> x : ", accel_angel_x, " y : ", accel_angel_y, " z : ", accel_angel_z
        print 
        print "                        < filter >"
        print "gyro  --> x : ", filtered_angel_x, " y : ", filtered_angel_y, " z : ", filtered_angel_z
        print "accel --> x : ", filtered_angel_x, " y : ", filtered_angel_y, " z : ", filtered_angel_z
        print 
        print "---------------------------------------------------------------"

except KeyboardInterrupt:
         GPIO.cleanup()
   
