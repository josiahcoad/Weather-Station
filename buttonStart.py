#!/usr/bin/python
import os, RPi.GPIO as GPIO, time

import RPi.GPIO as GPIO; GPIO.setwarnings(False); GPIO.setmode(GPIO.BCM)

red=12; btn = 21
GPIO.setup(btn,GPIO.IN)
GPIO.setup(red,GPIO.OUT)
GPIO.output(red, True)
status = not GPIO.input(btn) # the button is wired backwards...

while GPIO.input(btn) == True:	#Keep looping until the button gets pushed
   time.sleep(.05)					 #Give the cpu .05 sec between loop

os.system('python /home/pi/Weather_Log/Main.py')	#Run the Main program
