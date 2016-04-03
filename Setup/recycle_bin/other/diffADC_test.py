#!/usr/bin/python
from setup1115 import ADS1x15
from time import sleep
adc = ADS1x15(ic=0x01)
#range = float(raw_input("Pick your range in V:\
#\n6.144\n4.096\n2.048\n1.024\n0.512\n0.256\n>> "))
mVdiff = adc.readADCDifferential23(4096, 250)
question = raw_input("Are you plugged into 2 and 3? ")
#if question == "yes":
while True:
	mVdiff = adc.readADCDifferential23(4096, 250)
	print mVdiff
	sleep(.1)
