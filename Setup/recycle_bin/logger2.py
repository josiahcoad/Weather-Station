#!/usr/bin/python

'''~~~~~~~SETUP~~~~~~~~'''

#Import Libraries
#-Import Python Libraries
import time, os, signal, sys, inspect, RPi.GPIO as GPIO
from numpy import average as avg #Averaging function

#-Use a special function to allow the program to access libraries from a sub-folder
cmd_subfolder=os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile\
( inspect.currentframe() ))[0],"Setup")))
if cmd_subfolder not in sys.path:
     sys.path.insert(0, cmd_subfolder)

#-Import special libraries
from setup1115 import ADS1x15 #Pyrometer
from setupBME280 import * #BME280

#Setup for i2c Sensors
#-Assign the ADC 
adc = ADS1x15(ic= 0x01) #Analog to digital converter (Wind, SWave, etc.)
#-Assign the BME280
BME280 = BME280(mode=BME280_OSAMPLE_8) #BME280 (Pressure, temp, R/H)
#-Add conversion equations to convert raw mV data to intended units
def mVtoSW-WM2(mV_SWave):
    WM2 = mV_SWave * .250
    return WM2
def mVtoAngle(mV_windDir):
    angle = (mV_windDir/3319) * 360
    return angle
def mVtoSW-WM2(mV_SWave):
    WM2 = mV_SWave * .250
    return WM2
    
#Setup for Rain Sensor
#-Start the counter as a program running in the background
os.system('python Setup/setuptoggle.py &')
#-Setup the GPIO for the "un-toggler"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.IN) #17 takes the toggle input from the other file
GPIO.setup(27,GPIO.OUT) #27 will feed back in order to un-toggle it
mm_rain = 0 #This variable stores the total amount of water collected per minute

#Setup File Formatting
#-By default, Python generates some useless .pyc files 
#-Include a command that stops it from generating .pyc files
sys.dont_write_bytecode = True

#-Setup the header format for the files 
sensorHeader = ('{0:^30}{1:^30}{2:^30}{3:^30}{4:^30}{5:^30}{6:^30}'.format(\
'{ Internal Clock }', '{ Apogee Pyrometer }', '{ Ada. BME280 (For Internal) }', '{ TE525 Rain }',\
'{ Wind Monitor - MA 05106 }', '{ HYT-221 (For External) }', '{KIPP & ZONEN CGR3}',))
measureHeader = ('{0:^30}{1:^30}{2:^10}{3:^10}{4:^10}{5:^30}{6:^15}{7:^15}{8:^15}{9:^15}{10:^30}'.format(\
'Date & Time', 'SWave_Intensity', 'Air_Temp', 'Pressure', 'R/H', 'Rainfall',\
'Wind_Direction', 'Wind_Speed', 'Air_Temp', 'R/H', 'Longwave Radiation'))
unitHeader = ('{0:^30}{1:^30}{2:^10}{3:^10}{4:^10}{5:^30}{6:^15}{7:^15}{8:^15}{9:^15}{10:^30}'.format(\
'Year-Mnth-Day-Hr-Min-Sec', '[W/M^2]', '[C]', '[mBar]', '[%]', '[mm]',\
'[degrees]', '[m/s]', '[C]', '[%]', '[W/M^2]'))
#-Set the column formatting for the sensor values
            #datetime, WM2, degrees_C, mbar, humid, mm_rain, angle
columnSpacing = '{0:<30}{1:<30}{2:<10}{3:<10}{4:<10}{5:<30}{6:<15}{7:<15}{8:<15}{9:<15}{10:<30}'
#get rid of this->columnSpacing = '%s  %22.2f  %16.2f  %8.2f  %5.2f  %21.3f  %21.0f \n'

#Setup Variables for Time, # of Uploads, And # of Loops
#-Set the variable prevHour equal to 25
#-Set the variable prevMin equal to currentMin
prevHour, prevMin = 25, time.strftime('%M', time.gmtime())
#-Set number of uploads equal to 0
uploads = 0
#-Set total number of loops equal to 0
loopsTotal = 0

#Create Empty Lists
#-Create an empty list for each sensor in order to hold digital and converted data
SWaveList, tempList, mbarList, humidList, windDirList, LWaveList = [], [], [], [], [],[]
#-Create an empty list for each analog sensor in order to also hold mV raw data
mV_SWaveList, mV_windDirList, mV_LWaveList = [], [], []


#Create Program-Ender Function
def signal_handler(signal, frame):
    #-Close out of currently open files
    InputFile.close(); AvgFile.close(); RawFile.close()
    #-Upload the latest files to github
    os.system('git add . && git commit -m weatherLog && git push')
    #-Close the program
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



'''~~~~~~~LOOP~~~~~~~~'''
#Start the loop for checking and logging all of the sensors
while True:
    #Set Time Variables That Are to be Reset Every Loop Occurrence
    #-Set the variable startTime equal to the start of a time keeper
    startTime = time.time()
    #-Set the variable datetime equal to the formatted string of the current date and time
    datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime())
    #-Get current hour using the time library, set it equal to the currentHour 
    currentHour = time.strftime('%H', time.gmtime())
    #-Get current min using the time library, set it equal to the currentMin
    currentMin = time.strftime('%M', time.gmtime())
    
    #Read Sensors
    #-Read the input GPIO pin from the counter program running in the background
    if (GPIO.input(17) == True):
	    #-->If the pin is high, add 0.254 to the variable mm_rain
	    mm_rain += 0.254
	    #-->Pulse another pin as high so as to tell the background program to untoggle
	    GPIO.output(27, True)
    else:
        GPIO.output(27, False)
        
    #-Get the current ADC using the method set up in the setup (SWave, wind direction, etc)
    #-->Set the readings equal to a variable with the respective name
    mV_SWave = adc.readADCSingleEnded(0, 6144, 250)
    mV_windDir = adc.readADCSingleEnded(1, 6144, 250)
    mV_LWave = adc.readADCDifferential23(256, 250) #Raw mV data of Longwave Rad. (CGR3) using differential
    #-Get the current BME280 using the method set up in the setup (temp, pressure and R/H)
    #-->Set the readings equal to a variable with the respective name
    degrees_C = BME280.read_temperature()
    mbar = BME280.read_pressure() / 100
    humidity = BME280.read_humidity()
    
    #Change all the sensor values (currently floats) to strings for formatting later
    # Works like this: var1, var2, var3 = "%0.2f" %var1, "%0.4f" %var2, "%0.3f" %var3
    # The number on the left of the decimal is the number of digits to display to the left of the decimal
    degrees_C, mbar, humidity, WM2, angle, 
    mV_SWave, mV_windDir
    
    #Add the Current Sensor Data Value to its Respective Lists
    #-Append (aka store) the raw mV variable values to their respective lists
    mV_SWaveList.append(mV_SWave)     
    mV_windDirList.append(mV_windDir) 
    mV_LWaveList.append(mV_LWave)
    #-Append the digital/converted-analog variable values to respective lists
    SWaveList.append(mVtoSW-WM2(mV_SWave))
    tempList.append(degrees_C)
    mbarList.append(mbar)
    humidList.append(humidity)
    windDirList.append(mVtoAngle(mV_windDir))
    

    #Change in the Hour:
    #-Check to see if currentHour is not equal to prevHour
    if currentHour != prevHour:
        #-->Set prevHour equal to currentHour
        prevHour = currentHour
        #-->Check to see if loopsTotal is not equal to 0
        #-->If the number of loops does not equal zero, AKA it is not the first time through...
        if loopsTotal != 0: 
            #--->Close all files
 	        InputFile.close(); AvgFile.close(); RawFile.close()
 	        #--->Commit and upload the files to github
 	        os.system('git add . && git commit -m weatherLog && git push')
            #--->Add one to the total number of uploads 
            uploads += 1
        #-->Open new files (Input File, Raw File, Avg File) for logging
        fileTimeStamp = time.strftime('%Y-%m-%d Hr:%H', time.gmtime()) #Set up the proper formatting
        InputFile = open('dataInput/%s' % fileTimeStamp, 'w')
        AvgFile = open('dataAvgs/%s' % fileTimeStamp, 'w')
	    RawFile= open('dataAvgs/dataRaw/%s' % time.strftime('%Y-%m-%d Hr:%H', time.gmtime()), 'w')
        #-->Write the headers to the new files
        InputFile.write('%s\n%s\n%s\n' % (sensorHeader, measureHeader, unitHeader))
        AvgFile.write('%s\n%s\n%s\n' % (sensorHeader, measureHeader, unitHeader))
	    RawFile.write('%s\n%s\n%s\n' % (sensorHeader, measureHeader, unitHeader))
    
    #Change in the Minute:
    #-Check to see if currentMin is not equal to prevMin
    if currentMin != prevMin:
	    #-->Set prevMin equal to currentMin
	    prevMin = currentMin
	    #-->Write the average (and total amount of rain) of each list to the Avg File
        AvgFile.write(columnSpacing % (datetime, avg(SWaveList), avg(tempList), avg\
	                                            (mbarList), avg(humidList), mm_rain, avg(mVtoAngle(mV_windDir))))
	                                            
	    #-->Then clear the lists
	    SWaveList, tempList, mbarList, humidList, windDirList = [], [], [], [], []
        mV_SWaveList, mV_windDirList = [], []
	    #-->Set the variable which holds the total amount of rain back to zero
	    mm_rain = 0
    
	#-Write the current raw sensor values to the Raw File
	RawFile.write('%s, %15.2f, %10.4f\n' % (datetime, avg(mV_SWave), avg(mV_windDir)))
    #-Write the current sensor values to the Input File
    InputFile.write(columnSpacing % (datetime, mVtoSW-WM2(mV_SWave), degrees_C, mbar, humidity, mm_rain, mVtoAngle(mV_windDir)))
   
    #Add one to the total number of Loops that the program has run
    loopsTotal += 1
    #For viewing purposes: Prints a GM clock and the # of loops and # of uploads
    os.system('clear')
    print '%s\nTotal Loops Ran: %s\nUploads Completed: %s' % (time.strftime('%H:%M:%S', time.gmtime()), loopsTotal, uploads)
    
    #Wait (AKA Sleep) 1 second minus whatever time the process takes
    #  if the process takes more than 1 sec, don't sleep at all
    elapsedTime = time.time() - startTime
    if elapsedTime < 1 and elapsedTime > 0:
        time.sleep (1 - elapsedTime)
 
