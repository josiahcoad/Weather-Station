'''
================================================
Meterological Research Station - Dr. Ayal Anis
Created by Josiah Coad, '19
debugger.py - version 1.1 - 3/24/2016
PURPOSE:This program is for troubleshooting the each part
        of the weather station. It will take you systematically
	through each part. If something is wrong, it should 
        tell you.
================================================
'''

print "loading..."
import sys; sys.path.insert(0, '/home/pi/Weather_Log/Setup')
from call_sensors import *
import os

# Help Menu
helpmenu =  "\
=============================================================== \n\
        Howdy User. Welcome to the troubleshooter.              \n\
        You can test any part of the weather station.           \n\
        type 'x' to exit troubleshooter.                        \n\
        type 'help' at to see this menu again.                  \n\
        type 'clear' to clear the console.                      \n\
        ron (or roff)    | turn the red status light on.        \n\
        gon (or goff)    | turn the green status light off.     \n\
        btn              | display the status of the button.    \n\
        rain             | display the status of the toggle.    \n\
        cg               | display temp/LongWave -- CGR3.       \n\
        ap               | display ShortWave -- Apogee.         \n\
        wind             | displays wind direction.             \n\
        hyt              | displays temp/RH.                    \n\
        bme              | displays temp/RH/pressr.             \n\
        all              | does it all                          \n\
=============================================================== "

# LED Test
import RPi.GPIO as GPIO; GPIO.setwarnings(False); GPIO.setmode(GPIO.BCM)
red = 12; grn = 18
GPIO.setup(red,GPIO.OUT); GPIO.setup(grn,GPIO.OUT)
def testRed(x):
  GPIO.output(red, x)
def testGrn(x):
  GPIO.output(grn, x)

# Button Test
btn = 21
GPIO.setup(btn,GPIO.IN) 
def buttonStatus():
  status = not GPIO.input(btn)
  return ("Pressed") if status == True else ("Not Pressed")

# Rain Toggle
start_toggle_watch()
def toggleStatus():
  return ("Toggled") if rain_toggle_check(22) else ("Not Toggled")
  
# CGR3
from sensors_process import *
def testCGR3():
  CGR3_LW_V =  get_ABEdiff(7)              #Get the voltage of the temp from the CGR3
  CGR3_TH_V =  get_ABEdiff(8)              #Get the voltage of L-Wave radiatiation from the CGR3
  CGR3_TH_tempC = CGR3_V_to_tempC(CGR3_TH_V)  #Convert voltage to Celcius for the CGR3 thermister
  CGR3_LW_WM2 = CGR3_V_to_WM2(CGR3_LW_V)      #Convert voltage to WM2 for the CGR3 LW
  return ("CG3>> LW-WM2: %0.0f, temp: %0.2f" %(CGR3_LW_WM2, CGR3_TH_tempC))
# Apogee
def testApogee():
  Apg_SW_V = get_ABEdiff(5)                #Get the voltage of S-Wave raditaion from the Apogee
  Apg_SW_WM2 = Apogee_V_to_WM2(Apg_SW_V)      #Convert voltage to WM2 for the Apogee SW
  return ("APOGEE>> SW_WM2: %0.2f" %Apg_SW_WM2) 
# Wind Sensor
def testWind():
  Wind_dir_V = get_ABEdiff(6)                 #Get the voltage of the wind direction
  Wind_dir_angle = V_to_angle(Wind_dir_V)     #Convert voltage to angle for the wind direction
  return ("Wind Angle: %0.2f" %Wind_dir_angle)

c = "" #short for command
os.system('clear')
print helpmenu

#LOOP
while c != ("x"):
   c = raw_input("What would you like to try next: ")
   if c == "help": print helpmenu
   elif c == "clear": os.system('clear')

   elif c == "ron": testRed(True)
   elif c == "roff": testRed(False)
   elif c == "gon": testGrn(True)
   elif c == "goff": testGrn(False)
   elif c == "btn": print buttonStatus()
   elif c == "rain": print toggleStatus()
   elif c == "cg": print testCGR3()
   elif c == "ap": print testApogee()
   elif c == "wind": print testWind()
   elif c == "hyt": print "HYT221>> Temp: %0.2f RH: %0.2f" %get_HYT221()
   elif c == "bme": print "HYT221>> Temp: %0.2f Press: %0.2f RH: %0.2f" %get_BME280()
   elif c == "all": 
      testRed(True); testGrn(True); print buttonStatus(); print toggleStatus(); 
      print testWind(); print testApogee();
      print testCGR3()
      print "HYT221>> RH: %0.2f temp: %0.2f" %get_HYT221()
      print "BME280>> RH: %0.2f temp: %0.2f Press: %0.2f" %get_BME280()
   elif c == "x": print ("Thanks and Gig 'Em")
   else: print ("Not a valid option. Please try again.")
