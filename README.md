# Coanda-Effect-Drone-Rpi 
## Rpi 접속 <br>
<pre>
1. RPI 전원 연결
2. window 환경이라면, 원격데스크톱(remote desktop) 열기
3. 192.168.2.199 or 192.168.2.189 입력
4. shell 을 켠 뒤, cd CEDR
</pre>
![Alt text](/image/192.168.2.189.png "192.168.2.189"){: width="100" height="100"}
![Alt text](/image/192.168.2.199.png "192.168.2.199"){: width="100" height="100"}

## Class 사용법 <br>
### Servo.py 
Servo Motor Class <Br>
code example)
<pre>
from Servo import Servo

servo_1 = Servo(18, GPIO)     # Servo(pin, GPIO)
servo_2 = Servo(17, GPIO)     # pin is GPIO pin number

servo_1.motor_ctrl(argument)
</pre>



### Gyro.py
Gyro Class <Br>
code example)
<pre>
from Gyro import Gyro
gyro = Gyro()

accel_x, accel_y, accel_z = gyro.get_accel_data_g()
x_angle = gyro.get_x_rotation(accel_x, accel_y, accel_z)
y_angle = gyro.get_y_rotation(accel_x, accel_y, accel_z)

</pre>
<hr>

