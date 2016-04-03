#!/usr/bin/python

'''~~~~~~~SETUP~~~~~~~~'''
#User input:
#How many hours between uploads
userHour = int(raw_input('How many hours between uploading: '))
#How many minutes between averaging
userMin = int(raw_input('How many minutes between averaging: ')) 
#How many seconds between sensor pulling 
userSec = int(raw_input('How many seconds between pulling sensors: '))
print "Setting Up..." 

#Import Libraries
#-Import Python Libraries
import time, os, signal, sys, inspect, RPi.GPIO as GPIO
from numpy import average as avg #Averaging function

#-Use a special function to allow the program to access libraries from a sub-folder
cmd_subfolder=os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile\
( inspect.currentframe() ))[0],"Setup")))
if cmd_subfolder not in sys.path:
     sys.path.insert(0, cmd_subfolder)

#-Import these libraries
from setup1115 import ADS1x15 #Pyrometer
from setupBME280 import * #BME280

#Setup for i2c Sensors
#-Assign the ADC 
adc = ADS1x15(ic= 0x01) #Analog to digital converter (Wind, light, etc.)
#-Assign the BME280
BME280 = BME280(mode=BME280_OSAMPLE_8) #BME280 (Pressure, temp, R/H)
#-Add conversion equations to convert raw mV data to intended units
def mV_WM2(mV_light):
    WM2 = mV_light * 250
    return WM2
def mV_angle(mV_windDir):
    angle = (mV_windDir/3.319) * 360
    return angle
    
#Setup for Rain Sensor
#-Start the counter as a program running in the background
os.system('python Setup/setuptoggle.py &')
#-Setup the GPIO for the "un-toggler"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.IN)  #24 takes the toggle input from the other file
GPIO.setup(27,GPIO.OUT) #27 will feed back in order to un-toggle it
mm_rain = 0             #This variable stores the total amount of water collected per minute

#Setup File Formatting
#-By default, Python generates some useless .pyc files 
#-Include a command that stops it from generating .pyc files
sys.dont_write_bytecode = True

#-Setup the header format for the files 
sensorHeader = ('{0:^30}{1:^30}{2:^30}{3:^30}{4:^30}'.format(\
'{ Internal Clock }', '{ Apogee Pyrometer }', '{ Adafruit BME280 }', '{ TE525 Rain }', '{ Wind Monitor - MA 05106 }'))
measureHeader = ('{0:^30}{1:^30}{2:^10}{3:^10}{4:^10}{5:^30}{6:^15}{7:^15}'.format(\
'Date & Time', 'Light_Intensity', 'Air_Temp', 'Pressure', 'R/H', 'Rainfall', 'Wind_Direction', 'Wind_Speed'))
unitHeader = ('{0:^30}{1:^30}{2:^10}{3:^10}{4:^10}{5:^30}{6:^15}{7:^15}'.format(\
'Year-Mnth-Day-Hr-Min-Sec', '[W/M^2]', '[C]', '[mBar]', '[%]', '[mm]', '[degrees]', '[m/s]'))
#-Set the column formatting for the sensor values
            #datetime, WM2, degrees_C, mbar, humid, mm_rain, angle
columnSpacing = '%s  %22.2f  %16.2f  %9.2f  %7.2f  %18.3f  %21.0f \n'

#Setup Variables for Time, # of Uploads, And # of Loops
#-Set the variable prevHour equal to 25
#-Set the variable prevMin equal to currentMin
currentHour = int(time.strftime('%H', time.gmtime()))
prevHour = currentHour - userHour
#-Set the variable prevMin equal to currentMin plus (the users input minus one)
currentMin = int(time.strftime('%M', time.gmtime()))
prevMin = currentMin
#-Set number of uploads equal to 0
uploads = 0
#-Set total number of averages equal to 0
avgTotal = 0
#-Set total number of loops equal to 0
loopsTotal = 0

#Create Empty Lists
#-Create an empty list for each sensor in order to hold digital and converted data
lightList, tempList, mbarList, humidList, windDirList = [], [], [], [], []
#-Create an empty list for each analog sensor in order to also hold mV raw data
mV_lightList, mV_windDirList = [], []


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
    currentHour = int(time.strftime('%H', time.gmtime()))
    #-Get current min using the time library, set it equal to the currentMin
    currentMin = int(time.strftime('%M', time.gmtime()))
    
    #Read Sensors
    #-Read the input GPIO pin from the counter program running in the background
    if (GPIO.input(24) == True):
	    #-->If the pin is high, add 0.254 to the variable mm_rain
	    mm_rain += 0.254
	    #-->Pulse another pin as high so as to tell the background program to untoggle
            GPIO.output(27, True)
    else:
            GPIO.output(27, False)
        
    #-Get the current ADC using the method set up in the setup (light, wind direction, etc)
    #-->Set the readings equal to a variable with the respective name
    mV_light = adc.readADCSingleEnded(0, 6144, 250) / 1000
    mV_windDir = adc.readADCSingleEnded(1, 6144, 250) / 1000
    #-Get the current BME280 using the method set up in the setup (temp, pressure and R/H)
    #-->Set the readings equal to a variable with the respective name
    degrees_C = BME280.read_temperature()
    mbar = BME280.read_pressure() / 100
    humidity = BME280.read_humidity()
    
    #Add the Current Sensor Data Value to its Respective Lists
    #-Append (aka store) the raw mV variable values to their respective lists
    mV_lightList.append(mV_light)     #Raw mV data
    mV_windDirList.append(mV_windDir) #Raw mV data
    #-Append the digital/converted-analog variable values to respective lists
    lightList.append(mV_WM2(mV_light))
    tempList.append(degrees_C)
    mbarList.append(mbar)
    humidList.append(humidity)
    windDirList.append(mV_angle(mV_windDir))
    

    #Change in the Hour:
    #-Check to see if currentHour is equal to prevHour plus however many hours the user wants between logs
    if currentHour == prevHour + userHour:
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
        RawFile = open('dataAvgs/dataRaw/%s' % time.strftime('%Y-%m-%d Hr:%H', time.gmtime()), 'w')
        #-->Write the headers to the new files
        InputFile.write('%s\n%s\n%s\n' % (sensorHeader, measureHeader, unitHeader))
        AvgFile.write('%s\n%s\n%s\n' % (sensorHeader, measureHeader, unitHeader))
        RawFile.write('%s\n%s\n%s\n' % (sensorHeader, measureHeader, unitHeader))
    
    #Change in the Minute:
    #...Since currentMin is never higher than 59, the prevMin + the minutes between can't be more than 59.
    #-If prevMin + userMin is greater than 59, set prevMin equal to 
    if prevMin + userMin > 59:
            prevMin = 0 + (59 - (prevMin + userMin))
    #-Check to see if currentMin is equal to prevMin plus however many minutes the user wants between logs
    if currentMin == prevMin + userMin:
	    #-->Set prevMin equal to currentMin
            prevMin = currentMin
	    #-->Write the average (and total amount of rain) of each list to the Avg File
            AvgFile.write(columnSpacing % (datetime, avg(lightList), avg(tempList), avg\
	                                            (mbarList), avg(humidList), mm_rain, avg(mV_angle(mV_windDir))))
	                                            
	    #-->Then clear the lists
	    lightList, tempList, mbarList, humidList, windDirList = [], [], [], [], []
            mV_lightList, mV_windDirList = [], []
	    #-->Set the variable which holds the total amount of rain back to zero
	    mm_rain = 0
    	    avgTotal += 1
    #-Write the current raw sensor values to the Raw File
    RawFile.write('%s, %15.2f, %10.4f\n' % (datetime, avg(mV_light), avg(mV_windDir)))
    #-Write the current sensor values to the Input File
    InputFile.write(columnSpacing % (datetime, mV_WM2(mV_light), degrees_C, mbar, humidity, mm_rain, mV_angle(mV_windDir)))
   
    #Add one to the total number of Loops that the program has run
    loopsTotal += 1
    #For viewing purposes: Prints a GM clock and the # of loops and # of uploads
    os.system('clear')
    print '%s\nTotal Loops Ran: %s\nAverages Completed: %s\nUploads Completed: %s' % (time.strftime('%H:%M:%S', time.gmtime()), loopsTotal, avgTotal, uploads)
    print 'currentMin', currentMin, 'prevMin', prevMin, 'userMin', userMin

    #Wait (AKA Sleep) 1 second minus whatever time the process takes
    #  if the process takes more than 1 sec, don't sleep at all
    elapsedTime = time.time() - startTime
    if elapsedTime < 1 and elapsedTime > 0:
        time.sleep ((1 + (userSec-1)) - elapsedTime)

