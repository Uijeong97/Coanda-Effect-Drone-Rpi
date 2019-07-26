#import os, time

#os.system ("sudo pigpiod") #Launching GPIO library
#time.sleep(1) 

#import pigpio
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
