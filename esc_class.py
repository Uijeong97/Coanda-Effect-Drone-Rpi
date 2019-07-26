# origin file is esc.py ( /origin_code/esc.py )
# This file is a slight modification and classifying of the original file.
# If you want to use this class, do this in main code -> var = bldc_motor(ESC, max, min, start)

import os, time

os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) 

import pigpio

class bldc_motor:
    def __init__(self, ESC, max, min, start): #ESC=4
        self.ESC = ESC
        self.max_value = max # max speed
        self.min_value = min # min speed 
        self.init_speed = start # init speed
        self.pi = pigpio.pi();
        self.pi.set_servo_pulsewidth(ESC, 0) 
        

    def manual_drive(self): #You will use this function to program your ESC if required
        print "You have selected manual option so give a value between 0 and you max value"    
        while True:
            inp = raw_input()
            if inp == "stop":
                self.stop()
                break
            elif inp == "control":
                self.control()
                break
            elif inp == "arm":
                self.arm()
                break   
            else:
                self.pi.set_servo_pulsewidth(ESC,inp)

    def calibrate(self):   #This is the auto calibration procedure of a normal ESC
        self.pi.set_servo_pulsewidth(self.ESC, 0)
        print("Disconnect the battery and press Enter")
        inp = raw_input()

        if inp == '':
            self.pi.set_servo_pulsewidth(self.ESC, self.max_value)
            print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
            inp = raw_input()

        if inp == '':            
            self.pi.set_servo_pulsewidth(self.ESC, self.min_value)
            print "Wierd eh! Special tone"
            time.sleep(7)
            print "Wait for it ...."
            time.sleep (5)
            print "Im working on it, DONT WORRY JUST WAIT....."
            self.pi.set_servo_pulsewidth(self.ESC, 0)
            time.sleep(2)
            print "Arming ESC now..."
            self.pi.set_servo_pulsewidth(self.ESC, self.min_value)
            time.sleep(1)
            print "See.... uhhhhh"

            self.control() # You can change this to any other function you want

    def control(self): 
        print "I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'"
        time.sleep(1)
        speed = self.init_speed    # change your speed if you want to.... it should be between 700 - 2000
        print "Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed"

        while True:
            self.pi.set_servo_pulsewidth(self.ESC, speed)
            inp = raw_input()
            if inp == "q":
                speed -= 100    # decrementing the speed like hell
                print "speed = %d" % speed

            elif inp == "e":    
                speed += 100    # incrementing the speed like hell
                print "speed = %d" % speed

            elif inp == "d":
                speed += 10     # incrementing the speed 
                print "speed = %d" % speed

            elif inp == "a":
                speed -= 10     # decrementing the speed
                print "speed = %d" % speed
            elif inp == "stop":
                self.stop()          #going for the stop function
                break
            elif inp == "manual":
                self.manual_drive()
                break
            elif inp == "arm":
                self.arm()
                break   
            else:
                print "!! Press a,q,d or e"

    def arm(self): #This is the arming procedure of an ESC 
        print "Connect the battery and press Enter"
        inp = raw_input()    

        if inp == '':
            self.pi.set_servo_pulsewidth(self.ESC, 0)
            time.sleep(1)
            self.pi.set_servo_pulsewidth(self.ESC, self.max_value)
            time.sleep(1)
            self.pi.set_servo_pulsewidth(self.ESC, self.min_value)
            time.sleep(1)
            self.control()

    def stop(self): #This will stop every action your Pi is performing for ESC ofcourse.

        self.pi.set_servo_pulsewidth(self.ESC, 0)
        self.pi.stop()


         
