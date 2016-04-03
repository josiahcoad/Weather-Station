import sys; sys.path.insert(0, '/home/pi/Weather_Log/Setup/Sensors')



'''ABEdiff - 18 bit ADC'''
from ABEdiff_setup import ADCDifferentialPi
from ABEsmbus_setup import ABEHelpers
i2c_helper = ABEHelpers(); bus = i2c_helper.get_smbus()
ABEadc = ADCDifferentialPi(bus, 0x68, 0x69, 18)

from time import sleep
from ADC_conversions import *
import os
while True:
   V = ABEadc.read_voltage(6)
   angle = V*400.00
   print angle
   sleep(.1)
