
'''
================================================
Meterological Research Station - Dr. Ayal Anis
Created by Josiah Coad
call_sensors.py - version 1.1 - 3/4/2016 
PURPOSE:This library sets up sensors to be pulled 
	by the sensor_process library
Requires that python smbus be installed; also i2c enabled
================================================
'''

import sys; sys.path.insert(0, '/home/pi/Weather_Log/Setup/Sensors')

'''PULL SENSORS'''

#ANALOG SENSORS
'''ADS1115 - ADC'''
try: 
   from ADS1115_setup import ADS1x15; adc = ADS1x15(ic= 0x01) #Setup ADS1115
except IOError:
   print ("i2c ERROR. ADS1115. See Debug Doc to for help.")
def get_ADS1115(n):
	V = adc.readADCSingleEnded(n, 4096, 250) / 1000  #Read the ADC on channel 0
	return V

'''ABEdiff - 18 bit ADC'''
try:
   from ABEdiff_setup import ADCDifferentialPi
   from ABEsmbus_setup import ABEHelpers
   i2c_helper = ABEHelpers(); bus = i2c_helper.get_smbus()
   ABEadc = ADCDifferentialPi(bus, 0x68, 0x69, 18)
except IOError:
   print ("i2c ERROR. ABEdiff. See Debug Doc to for help.")
def get_ABEdiff(n):
        volts = ABEadc.read_voltage(n)
        return volts

#DIGITAL SENSORS
'''HYT_221 - RH/Temp'''
try:
   import smbus; add = 0x28; ansa = bytearray(); hyt = smbus.SMBus(1) #Setup HYT-221
except IOError:
   print ("i2c ERROR. HYT221. See Debug Doc to for help.")
def get_HYT221():
	ansa = hyt.read_i2c_block_data(add,4)                      #Read HYT-221
	hum = ansa[0]<<8 | ansa[1]; hum = hum & 0x3FFF             #Process Bits for RH
	ansa[3] = ansa[3] & 0x3F; temp = ansa[2] << 6 | ansa[3]    #Process Bits for Temp
	outRH = 100.0*hum/(2**14); outTemp = 165.0*temp/(2**14)-40 #Convert Bits for RH & Temp
	return outRH, outTemp

'''BME280 - RH/Temp/Pressure/'''
try:
   from BME280_setup import *; BME280 = BME280(mode=BME280_OSAMPLE_8)  #Setup BME280
except IOError:
   print ("i2c ERROR. BME280. See Debug Doc to for help.")
def get_BME280(): 
	inRH = BME280.read_humidity()           #Read RH
	inTemp = BME280.read_temperature()      #Read Temp
	pressure = BME280.read_pressure() / 100 #Read Pressure
	return inRH, inTemp, pressure

#RAIN TOGGLE
'''1115_ALRT - Toggle Rain Switch'''
import RPi.GPIO as GPIO
GPIO.setwarnings(False); GPIO.setmode(GPIO.BCM)  #Setup GPIO
ALRT_pin = 22; GPIO.setup(ALRT_pin,GPIO.IN)      
from ADS1115_setup import ADS1x15; adc = ADS1x15(ic= 0x01) #Setup ADS1115

#If channel 0 is above 2V, alrt (pin 22) will go low meaning there IS an alrt
#If channel 0 is below 1V, alrt (pin 22) will go high meaning there is no alrt
def start_toggle_watch():
	#Connect rain to channel 0 of the ADS1115
	adc.startSingleEndedComparator(0, 2000, 100, pga=4096, sps=250,\
	activeLow=True, traditionalMode=True, latching=True, numReadings=1)
def rain_toggle_check(pin):
	triggered = GPIO.input(pin) 
	adc.getLastConversionResults() #Reset the alrt pin by asking it to check channel 0 again
	start_toggle_watch()
	if triggered == 0: 	#Meaning if it has been tripped
		return True
	elif triggered == 1: 	#Meaning if it hasn't been tripped
		return False
