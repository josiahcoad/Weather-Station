#...There are two parts, the setup and the loop

'''~~~~~~~SETUP~~~~~~~~'''

#...What happens in the setup: Import libraries, setup sensors, setup file formatting, 
#setup variables for time and counters, create empty lists, and create a close-out 
#method.

'''Import Libraries'''
-Import Python Libraries
#...Sensor specific and custom libraries are in a subfolder
-Use a special function to allow the program to access libraries from a sub-folder
-Import these libraries

'''Setup for i2c Sensors'''
#...Each digital sensor (the ADC included) has its own library
#...Assign a method to call that sensor from the library, set it equal to a variable 
#that is the sensor’s name
-Assign the ADC 
-Assign the BME280
#...The analog sensors output an analog voltage. These values will be converted to 
#display their respective units according to some equation given by the sensor 
#documentation. 
-Add conversion equations to convert raw mV data to intended units

'''Setup for Rain Sensor'''
#...When rain fills one side of the see-saw, the see-saw tips and a magnet on the 
#see-saw, in passing, trips a reed switch for several hundredths of a second, 
#thus closing the circuit shortly. However, the program loop only checks each sensor 
#once every second.
#...My solution to this is another program which will run in the background. It’s sole 
#purpose will be to loop hundreds of times per second, checking for that very short 
#closing of the circuit as read by one of the GPIO pins. If it senses that it is closed, 
#it will set another GPIO pin to high and will keep it high until the main program 
#gets around to checking. When the main program registers it as high, it send a pulse 
#back to the counter program through yet another GPIO pin, telling the counter program 
#that it can un-toggle the toggled pin.
-Start the counter as a program running in the background
-Setup the GPIO for the “un-toggler”

'''Setup File Formatting'''
#...By default, Python generates some useless .pyc files 
-Include a command that stops Python from generating .pyc files
#...The files that the data gets written to needs to be easily read and understood by 
#both user and other computer programs such as Matlab. The best way to do this is by 
#formatting the data into columns. When a new file is opened, each column needs to be 
#given a header; three in fact. Each column gets a sensor name, a sensor object (what 
#its sensing) and units. These headers will be centered for ease of viewing.
-Setup the header format for the files 
#...The data also needs to be written in a certain format in columns under these headers. Unlike the 
#headers, the sensor values should not be centered but rather left-oriented so that the 
#first digits line up.
#...Second consideration for formatting the sensor values: The values are floats with 
#sometime 5 digits after the decimal place. We want to curb that to a standard two 
#digits.
#...Third consideration: Special care must be taken that the column formatting does 
#not shift when an extra digit is added in on the left of the decimal (ex. when 9 Celc. becomes 10 Celc. )
-Set the column formatting for the sensor values

Setup Variables for Time, # of Uploads, And # of Loops
...The current minute and current hour in GM time are pulled at the       beginning of every loop from the time library.
...As the program loops, prevHour and prevMin are compared to currentHour and currentMin. If they are not equal, that means the time has changed and certain action needs to take place. The prevHour/prevMin is then reassigned to the currentHour/currentMin.
...If the hour has changed, the current files are closed, the most current files are uploaded to github and new files are created.
...Since new files need to be created at the beginning of the program, prevHour needs to be originally set to a variable that currentHour will never be, such as 25.
-Set the variable prevHour equal to 25
...The previous minute will also be compared to the current minute every time the program loops. If prev min is not equal to current min, the data recorded over the course of that minute will be averaged and written to a file. However, because there is not a minutes worth of data to average the first time through, the prev min must originally be set to current minute.
-Set the variable prevMin equal to currentMin
...'uploads' is an integer that records the amount of uploads to github that have taken place.
-Set uploads equal to 0
...'loopsTotal' is an integer that records the total amount of times that the program loops.
-Set loopsTotal equal to 0

Create Empty Lists
...The data from the sensors are taken once a second. This is dictated by a loop that pulls data from each sensor and performs all necessary functions. At the end of the loop, the program waits for one second minus however long the loop took to perform. Within this loop, the sensor data is each added to a respective list (temp to the temp list, etc.). Once a minute passes, the program uses an averaging function to average all the floats within each list. As for setup, one empty list for each sensor must be created.
-Create an empty list for each sensor in order to hold digital and converted data
The results of these calculations are stored within the sensor data lists mentioned above. However, for the analog output sensors, the voltage data (measured in mV) will also be recorded in separate lists. Thus, if the equations become inaccurate, the raw voltage will still be recorded for these sensors.
-Create an empty list for each analog sensor in order to also hold mV raw data

Create Program-Ender Function
...By default, the user can close out of the program at any time, except that this is a cold hard stop to the program, wherever it is. Instead, we need a function that will take the CTRL + C user end-program command and run a specific code to properly close out of the program. It must do the following:
-Close out of currently open files
-Upload the latest files to github
-Close the program


'''~~~~~~~LOOP~~~~~~~~'''


...What happens in the loop: time and sensor values are retaken and set to respective variables, these variables are added to list which will be reset every minute.
...If the minute changes, the lists containing the values from the last minute are averaged and written to a file. If the hour changes, the files are all closed, uploaded and new ones are made.
...At the end of the loop, a logger on the screen gets updated, and it waits for the remainder of the second

Set Time Variables That Are to be Reset Every Loop Occurrence
...First, start a stopwatch to time the loop. At the end of the loop, the program will wait for one second minus whatever time the loop took. Thus, the program loops accurately every second.
-Set the variable startTime equal to the start of a time keeper

...The date and time are used often throughout the loop. Each data entry and data-average entry, and even the name of each file will have a stamp of the current time (GM time) and date. Instead of calling this formatted string each instance, the datetime variable is set equal to the current date and time as gotten from the time library.
-Set the variable datetime equal to the formatted string of the current date and time
...The current hour and minute are used in the loop in comparison with the prevhour and prevmin. If they are not equal (AKA new minute or new hour), the program performs certain tasks. Thus, each loop occurrence, the variable currentHour and currentMin need to be reassigned to their real-time values.
-Get current hour using the time library, set it equal to the currentHour 
-Get current min using the time library, set it equal to the currentMin

Read Sensors
...Finally, it’s time to read the sensors.
...Start with the rain sensor. It is read differently than the other sensors. It uses GPIO whereas all the other sensors use i2c (digital).
-Read the input GPIO pin from the counter program running in the background 
--If the pin is high, add 0.254 to the variable mm_rain
--Pulse another pin as high so as to tell the background program to untoggle
...Note: Even the analog sensors aren’t truly read by the Pi as analog. They are passed into an A-D converter and then fed into the Pi (through i2c) as digital values which the A-D library converts to represent analog input.
-Get the current ADC using the method set up in the setup (light, wind direction, etc)
--Set the readings equal to a variable with the respective name
-Get the current BME280 using the method set up in the setup (temp, pressure and R/H)
--Set the readings equal to a variable with the respective name


Add The Current Sensor Data Value to its Respective Lists
...Store the raw mV data and the digital/converted analog data all in separate lists
-Append (aka store) the raw mV variable values to their respective lists
-Append the digital/converted-analog variable values to respective lists

If There is a Change in The Hour
...prevHour is compared to currentHour. If they are not equal, that means the hour has changed AKA it is a new hour.
-Check to see if currentHour is not equals prevHour
...If they are not equal...
...The prevHour is reassigned to the currentHour so that they are again equal and will continue to be so until currentHour changes again.
--Set prevHour equal to currentHour
...We want to know if this is the first time through the loop (loopTotal equals 0). If so, there will be no files to close or upload.
--Check to see if loopsTotal is not equal to 0
...If the number of loops does not equal zero, AKA it is not the first time through…
---Close all files
---Commit and upload the files to github
---Add one to the total number of uploads 
...And whether it’s the first loop or not, still open new files for logging.
...The data will be stored in three separate files (and the files in three folders). The File Input (for digital and converted-analog readings) and File Raw (only containing the unconverted mV data) will be written to every second (every loop). The File Averages will only be written to once a minute.
--Open new files (Input File, Raw File, Avg File)
...Remember setting the format for the file headers in the setup?
--Write the headers to the new files

If There is a Change in the Minute
...prevMin is compared to currentMin. If they are not equal, that means the minute has changed AKA it is a new minute.
-Check to see if currentMin equals prevMin
...If they are not equal...
...The prevMin is reassigned to the currentMin so that they are again equal and will continue to be so until currentMin changes again.
--Set prevMin equal to currentMin
...It takes the average of the last minute’s worth of data for each sensor individually and writes those averages to a file
...For the rain sensor, it has been recording the total amount of rain fallen the past minute. Record this total.
--Write the average (and total amount of rain) of each list to the Avg File
--Then clear the lists
--Set the variable which holds the total amount of rain back to zero

Otherwise...
Regardless of if the hour or minute changed, the sensor input and raw sensor input still have to be written to their respective files
-Write the current sensor values to the Input File
-Write the current raw sensor values to the Raw File

Ending the Loop
-Add one to the total number of Loops that the program has run
...For viewing purposes: First, clear the screen, then print a gm clock, the # of loops and the # of logs
-Print datetime, loopsTotal, uploads
...Last but not least, get the time of the loop by taking the current time and subtracting the starting time from it. Set this equal to a variable elapsedTime.
...If, for some reason (the upload to github could be slow), the total time of the loop took more than a second, make a special condition to not wait.
...If the total time of the loop took less than a second (as it should), subtract the total time of the loop from a second and wait for that long.
-Check to see if elapsedTime is greater than 1
--if yes, don’t wait
-otherwise, sleep whatever time there is left in the second

