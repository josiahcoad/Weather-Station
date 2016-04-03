from sensors_process import *
def data():
	str_CGR3_LW_V, str_CGR3_TH_V, str_Wind_dir_V, str_Apg_SW_V = format_raw_analog_to_str()
	str_Apg_SW_WM2, str_Wind_dir_angle, str_CGR3_TH_tempC, str_CGR3_LW_WM2 = format_converted_analog_to_str()
	str_outRH, str_outTemp, str_inRH, str_inTemp, str_pressure, str_mm_rain = format_digital_to_str()
	print \
	# Raw Analog
	'str_CGR3_LW_V ='  +str_CGR3_LW_V,  '\n',\
	'str_CGR3_TH_V ='  +str_CGR3_TH_V,  '\n',\
	'str_Wind_dir_V =' +str_Wind_dir_V, '\n',\
	'str_Apg_SW_V ='   +str_Apg_SW_V,   '\n',\
	# Converted Analog
	'str_Apg_SW_WM2 ='     +str_Apg_SW_WM2,     '\n',\
	'str_Wind_dir_angle =' +str_Wind_dir_angle, '\n',\
	'str_CGR3_TH_tempC ='  +str_CGR3_TH_tempC,  '\n',\
	'str_CGR3_LW_WM2 ='    +str_CGR3_LW_WM2,    '\n',\
	# HYT221
	'str_outRH ='   +str_outRH,   '\n',\
	'str_outTemp =' +str_outTemp, '\n',\
	# BME280
	'str_inRH ='     +str_inRH,     '\n',\
	'str_inTemp ='   +str_inTemp,   '\n',\
	'str_pressure =' +str_pressure, '\n',\
	'str_mm_rain ='  +str_mm_rain,  '\n'

def averages():
	avg_CGR3_LW_V, avg_CGR3_TH_V, avg_Wind_dir_V, avg_Apg_SW_V = average_raw_analog_lists()
	avg_CGR3_LW_WM2, avg_CGR3_TH_tempC, avg_Apg_SW_WM2, avg_Wind_dir_angle = average_converted_analog_lists()
	avg_outRH, avg_outTemp, avg_inRH, avg_inTemp, avg_pressure, mm_rain = average_digital_lists()
        print \
        # Raw Analog
        'avg_CGR3_LW_V 	= '  	+ avg_CGR3_LW_V,  '\n',\
        'avg_CGR3_TH_V 	= ' 	+ avg_CGR3_TH_V,  '\n',\
        'avg_Wind_dir_V = '	+ avg_Wind_dir_V, '\n',\
        'avg_Apg_SW_V 	= ' 	+ avg_Apg_SW_V,   '\n',\
        # Converted Analog
        'avg_CGR3_LW_WM2    = '	+ avg_CGR3_LW_WM2,   '\n',\
        'avg_CGR3_TH_tempC  = '	+ avg_CGR3_TH_tempC, '\n',\
        'avg_Apg_SW_WM2     = '	+ avg_Apg_SW_WM2,    '\n',\
        'avg_Wind_dir_angle = '	+ avg_Wind_dir_angle,'\n',\
        # HYT221
        'avg_outRH    = '   	+ avg_outRH,   '\n',\
        'avg_outTemp  = '	+ avg_outTemp, '\n',\
        # BME280
        'avg_inRH     = '     	+ avg_inRH,     '\n'\
        'avg_inTemp   = '	+ avg_inTemp,   '\n'\
        'avg_pressure = ' 	+ avg_pressure, '\n'\
        'mm_rain      = '       + mm_rain,      '\n'

from os import system; import time
def display(loops, averages, uploads):
        system('clear')
        print '%s\nTotal Loops Ran: %s\nAverages Completed: %s\nUploads Completed: %s' \
              % (time.strftime('%H:%M:%S', time.gmtime()), loops, averages, uploads)	
