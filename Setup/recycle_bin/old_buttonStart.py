#!/usr/bin/python
import os, RPi.GPIO as GPIO, time
os.system("clear")

print "Hello User. Welcome to the Weather Station."
print "The red LED blinking says that the board is powered but no program running"
print "Just press the button to start the logging."
print "The red LED will stop blinking and the green will start blinking"

import RPi.GPIO as GPIO; GPIO.setwarnings(False); GPIO.setmode(GPIO.BCM)

red = 12 #this is the LED that says the board is powered but no program running
grn = 18 #this is the LED that says the program is running
GPIO.setup(red,GPIO.OUT)
GPIO.setup(grn,GPIO.OUT)

GPIO.output(red, True)

# Button Test
btn = 21
GPIO.setup(btn,GPIO.IN)
status = not GPIO.input(btn)

while GPIO.input(btn) == True:	#Keep looping until the button gets pushed
   time.sleep(.05)					 #Give the cpu .05 sec between loop

def grnOn():
   GPIO.output(red, False)
   GPIO.output(grn, True)	                  #Turn on the LED that says the program is running

os.system('python /home/pi/Weather_Log/Main.py')	#Run the Main program
