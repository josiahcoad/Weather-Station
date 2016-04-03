import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#23 = The input from the see-saw reed switch
#17 = The output to the main program ("Logger")
#25 = The input from the main program to reset
#When 23 triggers, 17 toggles True
#When 25 triggers, 17 toggles False
GPIO.setup(23,GPIO.IN)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(25,GPIO.IN)

#x = True
#x = not x

while True:
    if (GPIO.input(23) == True):
	GPIO.output(17, True)	
    if (GPIO.input(25) == True):
	GPIO.output(17, False)
    
#VAR = 12
#GPIO.setup(VAR,GPIO.OUT)
#GPIO.output(VAR, True)
