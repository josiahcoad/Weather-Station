'''
================================================
Meterological Research Station - Dr. Ayal Anis
Created by Josiah Coad
sensors.py - version 1.1 - 10/26/2016 
PURPOSE: This library pulls sensors and performs mulitple data processes
Requires that python smbus be installed and i2c enabled
================================================
'''

'''PULL SENSORS'''
from call_sensors import *
def call_analog_sensors():
    global CGR3_LW_V, CGR3_TH_V, Wind_dir_V, Apg_SW_V
    CGR3_TH_V =  get_ABEdiff(8)              #Get the voltage of L-Wave radiatiation from the CGR3
    CGR3_LW_V =  get_ABEdiff(7)              #Get the voltage of the temp from the CGR3
    Wind_dir_V = get_ABEdiff(6)              #Get the voltage of the wind direction
    Apg_SW_V = get_ABEdiff(5)                #Get the voltage of S-Wave raditaion from the Apogee
    return CGR3_LW_V, CGR3_TH_V, Wind_dir_V, Apg_SW_V
def call_digital_sensors():
    global outRH, outTemp, inRH, inTemp, pressure
    # HYT221
    outRH, outTemp = get_HYT221()            #Get outside relative humidity and temperature
    # BME280
    inRH, inTemp, pressure = get_BME280()    #Get inside RH, temp and pressure
    return outRH, outTemp, inRH, inTemp, pressure
def check_rain():
    global mm_rain
    triggered = rain_toggle_check(22) #Check if the rain gauge has been triggered since last loop using GPIO 22
    if triggered == True: #If the bucket tips, it will trigger ALRT to 0 then rain_toggle_check outputs True
	mm_rain += 0.254 #The amount of rain that it takes to tip the bucket
    return mm_rain
def call_sensors():
    call_analog_sensors()
    call_digital_sensors()

#Convert analog data
from ADC_conversions import *
def convert_raw_analog():
    global Apg_SW_WM2, Wind_dir_angle, CGR3_TH_tempC, CGR3_LW_WM2
    Apg_SW_WM2 = Apogee_V_to_WM2(Apg_SW_V)      #Convert voltage to WM2 for the Apogee SW
    Wind_dir_angle = V_to_angle(Wind_dir_V)     #Convert voltage to angle for the wind direction
    CGR3_TH_tempC = CGR3_V_to_tempC(CGR3_TH_V)  #Convert voltage to Celcius for the CGR3 thermister
    CGR3_LW_WM2 = CGR3_V_to_WM2(CGR3_LW_V)      #Convert voltage to WM2 for the CGR3 LW
    return Apg_SW_WM2, Wind_dir_angle, CGR3_TH_tempC, CGR3_LW_WM2

'''DATA PROCESSING'''
#Make Empty lists
def make_empty_raw_analog_lists():
    global CGR3_LW_V_list, CGR3_TH_V_list, Wind_dir_V_list, Apg_SW_V_list
    CGR3_LW_V_list, CGR3_TH_V_list         = [], []      #Clear the lists for the CGR3
    Wind_dir_V_list, Apg_SW_V_list         = [], []      #Clear the lists for the wind and apogee
    return CGR3_LW_V_list, CGR3_TH_V_list, Wind_dir_V_list, Apg_SW_V_list
def make_empty_converted_analog_lists():
    global CGR3_LW_WM2_list, CGR3_TH_tempC_list, Wind_dir_angle_list, Apg_SW_WM2_list
    CGR3_LW_WM2_list, CGR3_TH_tempC_list   = [], []	 #Clear the lists for the CGR3
    Wind_dir_angle_list, Apg_SW_WM2_list   = [], []      #Clear the lists for the wind and apogee
    return CGR3_LW_WM2_list, CGR3_TH_tempC_list, Wind_dir_angle_list, Apg_SW_WM2_list
def make_empty_digital_lists():
    global outRH_list, outTemp_list, inRH_list, inTemp_list, pressure_list, mm_rain 
    outRH_list, outTemp_list               = [], []      #Clear the lists for outside RH and temp-HYT221
    inRH_list, inTemp_list, pressure_list  = [], [], []  #Clear the lists for inside RH, temp and pressure-BME280
    mm_rain = 0 #Set the variable which holds the total amount of rain back to zero
    return outRH_list, outTemp_list, inRH_list, inTemp_list, pressure_list, mm_rain
def make_empty_lists():
	make_empty_raw_analog_lists()
	make_empty_converted_analog_lists()
	make_empty_digital_lists()

#Add data to lists
def add_data_to_lists():
    # Raw Analog
    CGR3_LW_V_list.append(CGR3_LW_V)
    CGR3_TH_V_list.append(CGR3_TH_V)
    Wind_dir_V_list.append(Wind_dir_V)
    Apg_SW_V_list.append(Apg_SW_V)
    # Converted Analog
    CGR3_LW_WM2_list.append(CGR3_LW_WM2)
    CGR3_TH_tempC_list.append(CGR3_TH_tempC)
    Apg_SW_WM2_list.append(Apg_SW_WM2)
    Wind_dir_angle_list.append(Wind_dir_angle)
    # HYT221
    outRH_list.append(outRH)
    outTemp_list.append(outTemp)
    # BME280
    inRH_list.append(inRH)
    inTemp_list.append(inTemp)
    pressure_list.append(pressure)    

#Average the data; Return results as string
from numpy import average as avg
def average_raw_analog_lists():
	global avg_CGR3_LW_V, avg_CGR3_TH_V, avg_Wind_dir_V, avg_Apg_SW_V
	avg_CGR3_LW_V  = '%0.2f' %avg(CGR3_LW_V_list)
        avg_CGR3_TH_V  = '%0.2f' %avg(CGR3_TH_V_list)
        avg_Wind_dir_V = '%0.2f' %avg(Wind_dir_V_list)
        avg_Apg_SW_V   = '%0.2f' %avg(Apg_SW_V_list)
	return avg_CGR3_LW_V, avg_CGR3_TH_V, avg_Wind_dir_V, avg_Apg_SW_V
def average_converted_analog_lists():
	global avg_CGR3_LW_WM2, avg_CGR3_TH_tempC, avg_Apg_SW_WM2, avg_Wind_dir_angle
        avg_CGR3_LW_WM2   = '%0.2f' %avg(CGR3_LW_WM2_list)
        avg_CGR3_TH_tempC = '%0.2f' %avg(CGR3_TH_tempC_list)
        avg_Apg_SW_WM2    = '%0.2f' %avg(Apg_SW_WM2_list)
        avg_Wind_dir_angle    = '%0.2f' %avg(Wind_dir_angle_list)
	return avg_CGR3_LW_WM2, avg_CGR3_TH_tempC, avg_Apg_SW_WM2, avg_Wind_dir_angle
def average_digital_lists():
	global avg_outRH, avg_outTemp, avg_inRH, avg_inTemp, avg_pressure
	# HYT221
        avg_outRH   = '%0.2f' %avg(outRH_list)
        avg_outTemp = '%0.2f' %avg(outTemp_list)
        # BME280
        avg_inRH     = '%0.2f' %avg(inRH_list)
        avg_inTemp   = '%0.2f' %avg(inTemp_list)
        avg_pressure = '%0.2f' %avg(pressure_list)
        str_mm_rain = str(mm_rain)
	return avg_outRH, avg_outTemp, avg_inRH, avg_inTemp, avg_pressure, str_mm_rain
def average_lists():
  	average_raw_analog_lists()
	average_converted_analog_lists()
	average_digital_lists()

#Change data to a formatted string
def format_raw_analog_to_str():
	global str_CGR3_LW_V, str_CGR3_TH_V, str_Wind_dir_V, str_Apg_SW_V
	str_CGR3_LW_V  = '%0.2f' %CGR3_LW_V
	str_CGR3_TH_V  = '%0.2f' %CGR3_TH_V
	str_Wind_dir_V = '%0.2f' %Wind_dir_V
	str_Apg_SW_V   = '%0.2f' %Apg_SW_V
	return str_CGR3_LW_V, str_CGR3_TH_V, str_Wind_dir_V, str_Apg_SW_V
def format_converted_analog_to_str():
	global str_Apg_SW_WM2, str_Wind_dir_angle, str_CGR3_TH_tempC, str_CGR3_LW_WM2
	str_Apg_SW_WM2     = '%0.2f' %Apg_SW_WM2
	str_Wind_dir_angle = '%0.2f' %Wind_dir_angle
	str_CGR3_TH_tempC  = '%0.2f' %CGR3_TH_tempC
	str_CGR3_LW_WM2    = '%0.2f' %CGR3_LW_WM2
	return str_Apg_SW_WM2, str_Wind_dir_angle, str_CGR3_TH_tempC, str_CGR3_LW_WM2
def format_digital_to_str():
	global str_outRH, str_outTemp, str_inRH, str_inTemp, str_pressure, str_mm_rain
	str_outRH    = '%0.2f' %outRH 
	str_outTemp  = '%0.2f' %outTemp
	str_inRH     = '%0.2f' %inRH
	str_inTemp   = '%0.2f' %inTemp
	str_pressure = '%0.2f' %pressure
	str_mm_rain  = str(mm_rain) 
	return str_outRH, str_outTemp, str_inRH, str_inTemp, str_pressure, str_mm_rain
def format_data_to_str():
	format_raw_analog_to_str()
	format_converted_analog_to_str()
	format_digital_to_str()

#Switch off the GRN LED and turn on RED one on program close
import RPi.GPIO as GPIO; GPIO.setwarnings(False); GPIO.setmode(GPIO.BCM)

def controlLED(cmd):
   red=12; grn = 18
   GPIO.setup(red,GPIO.OUT)
   GPIO.setup(grn,GPIO.OUT)
   if cmd == "start":
      GPIO.output(red, False)
      GPIO.output(grn, True)
   elif cmd == "kill":
      GPIO.output(red, True)
      GPIO.output(grn, False)
#Just run this to see if any error messages pop up
def test_lib():
	call_analog_sensors()
	call_digital_sensors()
	make_empty_lists()
	convert_raw_analog()
	add_data_to_lists()
	average_lists()
	format_data_to_str()			
		
