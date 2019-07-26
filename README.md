# Coanda-Effect-Drone-Rpi 
## Rpi 접속 <br>
<pre>
1. RPI 전원 연결
2. window 환경이라면, 원격데스크톱(remote desktop) 열기
3. 192.168.2.199 or 192.168.2.189 입력
4. shell 을 켠 뒤, cd CEDR
</pre>

<img src="/image/192.168.2.189.png" title="192.168.2.189" width="300" height="300"> <img src="/image/192.168.2.199.png" title="192.168.2.199" width="300" height="300">

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



## RPi - Device(including Sensor) 연결 <br>
### RPi GPIO
<img src="/image/GPIO.png" title="BLDC" width="300" height="300">
<br>


### BLDC Motor
<img src="/image/BLDC.png" title="BLDC" width="500" height="300">
<pre>
검정선 -> Raspberrypi GND
흰선   -> Raspberrypi GPIO
</pre>
<br>


### Servo Motor
<img src="/image/Servo.PNG" title="Servo" width="400" height="300">
<pre>
빨간선 -> Raspberrypi Voltage, 3.3V or 5V 
주황선 -> Raspberrypi GPIO 
갈색선 -> Raspberrypi GND 
</pre>
<br>


### Gyro Sensor
<img src="/image/Gyro.png" title="Gyro" width="400" height="300">
<pre>
GYRO VCC  –> Raspberrypi Vortage, 3.3V or 5V
GYRO GND  –> Raspberrypi GND
GYRO SCL  –> Raspberrypi SCL
GYRO SDA  –> Raspberrypi SDA
</pre>
<br>


### GPS Sensor
<img src="/image/GPS.png" title="Gyro" width="400" height="300">
<pre>
GYRO VCC  –> Raspberrypi Vortage, 3.3V or 5V
GYRO GND  –> Raspberrypi GND
GYRO SCL  –> Raspberrypi SCL
GYRO SDA  –> Raspberrypi SDA
</pre>
