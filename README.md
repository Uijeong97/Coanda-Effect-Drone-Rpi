# Coanda-Effect-Drone-Rpi 

### Servo.py
Servo Motor Class
code example)
<pre>
from Servo import Servo

servo_1 = Servo(18, GPIO)     # Servo(pin, GPIO)
servo_2 = Servo(17, GPIO)     # pin is GPIO pin number

servo_1.motor_ctrl(argument)
</pre>

### Gyro.py
Gyro Class
code example)
<pre>
from Gyro import Gyro
gyro = Gyro()

accel_x, accel_y, accel_z = gyro.get_accel_data_g()
x_angle = gyro.get_x_rotation(accel_x, accel_y, accel_z)
y_angle = gyro.get_y_rotation(accel_x, accel_y, accel_z)

</pre>
