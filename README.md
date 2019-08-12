# Coanda-Effect-Drone-Rpi 
## Rpi 접속 <br>
<pre>
1. RPI 전원 연결
2. window -> 원격데스크톱(remote desktop) 열기
   Mac OS -> microsoft remote desktop 어플 다운 
3. 192.168.2.199 or 192.168.2.189 입력
4. shell 을 켠 뒤, cd CEDR

* 와이파이 연결이 KSQ Student 로 되어있어야 함
</pre>

<img src="/image/192.168.2.189.png" title="192.168.2.189" width="300" height="300"> <img src="/image/192.168.2.199.png" title="192.168.2.199" width="300" height="300">

<hr><br><br>

## Class 사용법 <br>

### bldc_motor.py
Bldc Motor Class <Br>
code example(test_class.py)
<pre>
from esc_class import bldc_motor

var = bldc_motor(4, 2000, 700, 800)
print "For first time launch, select calibrate"
print "Type the exact word for the function you want"
print "calibrate OR manual OR control OR arm OR stop"

inp = raw_input()
if inp == "manual":
    var.manual_drive()
elif inp == "calibrate":
    var.calibrate()
elif inp == "arm":
    var.arm()
elif inp == "control":
    var.control()
elif inp == "stop":
    var.stop()
else :
    print "Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!"
</pre>


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
<hr><Br><br>



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
