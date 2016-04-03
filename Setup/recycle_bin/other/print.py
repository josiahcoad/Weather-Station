#!/usr/bin/python

'''~~~~~~~SETUP~~~~~~~~'''

import time, os, signal, sys, inspect
from setup1115 import ADS1x15 #Pyrometer
from setupBME280 import * #BME280
from numpy import average as avg

#Strings for file writing
logHeader = 'New Sensor Input Log Initiated on'
sensorHeader = '     { Date & Time }       { APOGEE PYROMETER }        { Adafruit BME280 }   '
unitHeader =   'Year-Mnth-Day-Hr-Min-Sec--||------W/M^2-------||--celcius---mbar--------%hum\
id--||--mm_of_Rain--||--Wind_Direction--Wind_Speed(m/s)'
datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime())

#For changing process based on  hour/minute
prevHour = time.strftime('%H', time.gmtime())
prevMin = time.strftime('%M', time.gmtime())

#Creating lists that will contain data for averaging purpose
lightData = []
tempData = []
mbarData = []
humidData = []

#Special close out system 'Press Ctrl+C to exit'
def signal_handler(signal, frame):
    os.system('rm *pyc')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

os.system('clear') #Clears the screen

#Prints so you can see the output
print logHeader
print sensorHeader
print unitHeader + '\n'

while True:
    #Start the timer to time process
    startTime = time.time()
    #Get the current time
    datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime())
    hour = time.strftime('%H', time.gmtime())
    min = time.strftime('%M', time.gmtime())

    #These variables make it more convinient to pull the sensors
       #Pyrometer
    adc = ADS1x15(ic= 0x01)
    mV = adc.readADCSingleEnded(0, 6144, 250) / 1000
    WM2 = mV * 250
       #Adafruit BME280
    sensor = BME280(mode=BME280_OSAMPLE_8)
    degrees_C = sensor.read_temperature()
    mbar = sensor.read_pressure() / 100
    humidity = sensor.read_humidity()

    #Add the most recent data to the list for averaging purposes
    lightData.append(WM2)
    tempData.append(degrees_C)
    mbarData.append(mbar)
    humidData.append(humidity)
    
    columnSpacing = '%s %14.2f %16.2f %9.2f %10.2f' #datetime, WM2, degrees_C, mbar, humidity

    #When the hour changes, it's time to close the current file and start a new one
    if hour != prevHour:
        prevHour = hour
	print "\n\n Upload \n\n"

    #When the minute changes, it logs the average and the real time data
    if min != prevMin:
        prevMin = min
        print '\n\n' + columnSpacing + '\n\n' % (datetime, avg(lightData), avg(tempData), avg\
        (mbarData), avg(humidData))

    #Otherwise, it continues logging the real time data
    print columnSpacing % (datetime, WM2, degrees_C, mbar, humidity)
    
    #Wait (AKA Sleep) 1 second minus whatever time the process takes
    #  if the process takes more than 1 sec, sleep default to 1 sec
    elapsedTime = time.time() - startTime
    if elapsedTime < 1 and elapsedTime > 0:
	time.sleep (1 - elapsedTime)
    else:
	sleep (1)




