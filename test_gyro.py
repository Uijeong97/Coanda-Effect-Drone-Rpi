import Gyro as Gyro
 
gyro = Gyro()
 
def calc_average(gyro_xout, gyro_yout, gyro_zout, accel_xout, accel_yout, accel_zout):
   
    num_readings = 10;

    print "Starting Calibration"

    for i in range (num_readings):
        gyro_xout, gyro_yout, gyro_zout += gyro.get_gyro_data_lsb()
        accel_xout, accel_yout, accel_zout += gyro.get_accel_data_lsb()
        delay(100)

    accel_xout /= num_readings
    accel_yout /= num_readings
    accel_zout /= num_readings
    gyro_xout /= num_readings
    gyro_yout /= num_readings
    gyro_zout /= num_readings

    # Store the raw calibration values globally

    base_x_accel = accel_xout
    base_y_accel = accel_yout 
    base_z_accel = accel_zout 
    base_x_gyro = gyro_xout
    base_y_gyro = gyro_yout
    base_z_gyro = gyro_zout

    print "Finishing Calibration"

    return [base_x_gyro, base_y_gyro, base_z_gyro, base_x_accel, base_y_accel, base_z_accel]


try:
    while True:
                time.sleep(1)
                print "--------------------------------------------------------"
                print "=>init gyro data"
                print "---------"
                gyro_xout, gyro_yout, gyro_zout = gyro.get_gyro_data_lsb()
                print "gyro_xout: ", gyro_xout
                print "gyro_yout: ", gyro_yout
                print "gyro_zout: ", gyro_zout
                print
                print "=> init accelerometer data"
                print "------------------"
                accel_xout, accel_yout, accel_zout = gyro.get_accel_data_lsb()
                print "accel_xout: ", accel_xout, 
                print "accel_yout: ", accel_yout, 
                print "accel_zout: ", accel_zout, 
                print
                print "Confirm accel_zout is near by 16384 --> then OK" 
                print "--------------------------------------------------------"
                print
                print "보정 값"
                print "--------------------------------------------------------"

except KeyboardInterrupt:

     GPIO.cleanup()

 