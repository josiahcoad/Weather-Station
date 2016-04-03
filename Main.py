#!/usr/bin/python
'''
================================================
Meterological Research Station - Dr. Ayal Anis
Created by Josiah Coad
sensors.py - version 1.0 - 3/2/2016

PURPOSE: Pull sensors, average results, write to files, upload data

For a full list of sensors pulled plus other details, refer to README
================================================
'''

print "loading..."

'''~~~~~~~SETUP~~~~~~~~'''
import time
import sys; sys.path.insert(0, '/home/pi/Weather_Log/Setup') #import libs from sub folder
import sensors_process as process #a library w/ the functions for processing sensor data
import file_functions as files    #a library for file opening, writing, closing & uploading 
import signal, os
# Submit to a Runtimelog the time that the main program started 
os.system('echo "Start:" $(date) >> /home/pi/Weather_Log/data_Archives/Runtimelog.txt')
#Turn the green LED on & red off to signify the program is running
process.controlLED("start") #To signify that the program is not running

files.upload()

def killMain():
   files.close()
   files.upload()
   os.system("clear")
   print "\n\n\n"
   print "----------------------------------------"
   print "    Program Safetly Exited. Gig 'Em.    "
   print "----------------------------------------"
   process.controlLED("kill") #Turn the green LED off & red on to signify the program NOT running
   os.system('echo "Stop:" $(date) >> /home/pi/Weather_Log/data_Archives/Runtimelog.txt')
   sys.exit(0)   #exit the program

#a function to end the code properly by pressing ctrl+c
def signal_handler(signal, frame): 
   killMain()
signal.signal(signal.SIGINT, signal_handler)

files.opener() #Open the input and avg file in folder w/ the datetime as header
files.write_headers()

loops = 0
averages = 0 
uploads = 0  

process.start_toggle_watch()  #Start the ADS1115 looking for a rain trigger on channel 0
process.make_empty_lists()    #Start empty lists to hold the data to be averaged 
                              #also, sets the mm_rain = 0

#It is adviced at this point to wait at least 4 seconds between looping
#Reason: the loop takes about 1.2 seconds and w/ uploading, takes 3.2
desired_loop_time    = 5	#number of seconds between looping
desired_average_time = 59	#number of seconds between averaging
desired_upload_time  = 60	#number of seconds between uploading

average_time = time.time() + desired_average_time #set avg timer to zero
upload_time = time.time() + desired_upload_time   #set upload timer to zero

'''~~~~~~~LOOP~~~~~~~~'''
maxlooptime = 0
while True:
   starttime = time.time()
   loop_time = time.time() + desired_loop_time #set loop timer to zero
 
   process.call_sensors()
   process.check_rain()
   process.convert_raw_analog()
   pressure_list = process.add_data_to_lists() 
   process.format_data_to_str()
   files.write_inputs()    
   files.write_raw()
   
   if time.time() > upload_time:
	   files.close()
	   files.upload()
	   files.opener()
	   files.write_headers()
	   upload_time = time.time() + desired_upload_time #set upload timer to zero
	   uploads += 1    

   if time.time() > average_time:	
      process.average_lists()
      files.write_averages()
      process.make_empty_lists()
      average_time = time.time() + desired_average_time #set avg timer to zero
      averages += 1
    
   loops += 1 
   os.system('clear') #Print the time, total loops, averages and uploads onto the console
   print '%s\nTotal Loops Ran: %s\nAverages Completed: %s\nUploads Completed: %s' \
      % (time.strftime('%H:%M:%S', time.gmtime()), loops, averages, uploads)
   looptime = (time.time()-starttime)
   if looptime > maxlooptime:
      maxlooptime = looptime
   print 'Code Execution time: %0.2f\n' %maxlooptime
   files.print_inputs()
   if time.time() < loop_time: #as long as it didn't take longer than the desired time per loop...
	   time.sleep(loop_time - time.time()) #Wait for the rest of the desired second(s) before looping again
