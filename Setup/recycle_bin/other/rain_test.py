#The rain will fill up a "bucket". The bucket is attached to a see-saw.
#Once the rain fills up the bucket, the see-saw totters.
#The see-saw has a magnet on it that passes by a reed switch.
#Notice: This switch is not toggle.
#Thus, an arduino (or a flip-flop IC) will be used pull the signal high
#when the reed-switch triggers.

#OK, so each time the loop occurs on the pi (every one second),
#one of the GPIO pins must be checked, lets call it "rain_boolean".
#If the value of the pin is high, that means that it has been triggered
#Say that one bucket holds 60 ml of water...
#It will add 60 to the overall variable of "ml_rain"
#THEN, It will send a high out of another pin to tell the arduino to
#set the "rain_boolean" to low again

#So for logging, it will log whatever number the variable "raintest" is 
#in the dataInput file
#When it comes time to average the past minute's results,
#It will log the total "ml_rain" for the last minute
#Finally it will reset the variable "ml_rain" to zero
#...and so it will repeat every minute
import os
from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
os.system('python Setup/toggle.py &')
GPIO.setmode(GPIO.BCM)
#17 takes the toggle input from the other file
#27 will feed back in order to un-toggle it
GPIO.setup(17,GPIO.IN)
GPIO.setup(27,GPIO.OUT)

ml_rain = 0
while True:
    if (GPIO.input(17) == True):
	ml_rain += 60
	GPIO.output(27, True)
	print ml_rain
    else:
	GPIO.output(27, False) 
    sleep(1)
    	print ml_rain
	fileAvg.write('...,10.0f,...' %(...ml_rain))
	ml_rain = 0 	
    else:
	fileAvg.write('...,10.0f,...' %(...ml_rain))
    sleep(5)
    -'''
