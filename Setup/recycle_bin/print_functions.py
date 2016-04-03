import time
from sensors_process import *
from file_functions import get_headers, get_columnSpacing; get_headers(); get_columnSpacing()


from os import system 
def print_headers():
   print (sensorHeader+'\n'+measureHeader+'\n'+unitHeader)

def print_inputs():
   str_Apg_SW_WM2, str_Wind_dir_angle, str_CGR3_TH_tempC, str_CGR3_LW_WM2 = format_converted_analog_to_str()
   str_outRH, str_outTemp, str_inRH, str_inTemp, str_pressure, str_mm_rain = format_digital_to_str()
   datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime()) #get the current date and time
   print('\n'+columnSpacing.format(datetime, str_Apg_SW_WM2, str_inTemp, str_pressure, str_inRH, \
   str_mm_rain, str_Wind_dir_angle, 'no_Speed', str_outTemp, str_outRH, str_CGR3_LW_WM2, str_CGR3_TH_tempC))

