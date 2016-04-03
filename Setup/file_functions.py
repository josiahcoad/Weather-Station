import time
from sensors_process import *

columnSpacing = '{0:<30}{1:<30}{2:<10}{3:<10}{4:<10}{5:<17}{6:<15}{7:<15}{8:<15}{9:<15}{10:<15}{11:<30}'

sensorHeader = ('{0:<30}{1:<30}{2:<30}{3:<17}{4:<30}{5:<30}{6:<30}'.format\
('{ Internal Clock }', '{ Apogee Pyrometer }', '{ Ada. BME280 (Inside) }', '{ TE525 Rain }', '{ Wind Monitor - MA 05106 }', '{ HYT-221 (Outside) }', '{KIPP & ZONEN CGR3}',))
measureHeader = (columnSpacing.format\
('Date & Time', 'SWave_Radiation', 'In_Temp', 'Pressure', 'in_R/H', 'Rainfall', 'Wind_Dir.', 'Wind_Speed', 'out_Temp', 'out_R/H', 'LWave_Rad.', 'CGR3_temp'))
unitHeader = (columnSpacing.format\
('Year-Mnth-Day-Hr-Min-Sec', '[W/M^2]', '[C]', '[mBar]', '[%]', '[mm]', '[degrees]', '[m/s]', '[C]', '[%]', '[W/M^2]','[C]'))
Raw_unitHeader = (columnSpacing.format\
('Year-Mnth-Day-Hr-Min-Sec', '[V]', '[C]', '[mBar]', '[%]', '[mm]', '[V]', '[m/s]', '[C]', '[%]', '[V]','[V]'))

def opener():
   global InputFile, AvgFile, RawFile
   fileTimeStamp = time.strftime('%Y-%m-%d Hr:%H', time.gmtime()) #Set up the proper formatting
   InputFile = open('/home/pi/Weather_Log/data_Archives/dataInput/%s' % fileTimeStamp, 'w') 
   AvgFile = open('/home/pi/Weather_Log/data_Archives/dataAvgs/%s' % fileTimeStamp, 'w')
   RawFile = open('/home/pi/Weather_Log/data_Archives/dataRaw/%s' % fileTimeStamp, 'w')
   return InputFile, AvgFile, RawFile

def write_headers():
   InputFile.write(sensorHeader+'\n'+measureHeader+'\n'+unitHeader)
   AvgFile.write(sensorHeader+'\n'+measureHeader+'\n'+unitHeader)
   RawFile.write(sensorHeader+'\n'+measureHeader+'\n'+Raw_unitHeader)

def write_averages():
   avg_CGR3_LW_WM2, avg_CGR3_TH_tempC, avg_Apg_SW_WM2, avg_Wind_dir_angle = average_converted_analog_lists()
   avg_outRH, avg_outTemp, avg_inRH, avg_inTemp, avg_pressure, str_mm_rain = average_digital_lists()
   datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime()) #get the current date and time
   AvgFile.write('\n'+columnSpacing.format(datetime, avg_Apg_SW_WM2, avg_inTemp, avg_pressure, avg_inRH, \
   str_mm_rain, avg_Wind_dir_angle, 'nan', avg_outTemp, avg_outRH, avg_CGR3_LW_WM2, avg_CGR3_TH_tempC)) 

def get_data(): # An idea for later
   global data 
   datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime()) #get the current date and time
   str_Apg_SW_WM2, str_Wind_dir_angle, str_CGR3_TH_tempC, str_CGR3_LW_WM2 = format_converted_analog_to_str()
   str_outRH, str_outTemp, str_inRH, str_inTemp, str_pressure, str_mm_rain = format_digital_to_str()
   data = datetime, str_Apg_SW_WM2, str_inTemp, str_pressure, str_inRH, \
   str_mm_rain, str_Wind_dir_angle, 'nan', str_outTemp, str_outRH, str_CGR3_LW_WM2, str_CGR3_TH_tempC
   return data

def write_inputs():
   datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime()) #get the current date and time
   str_Apg_SW_WM2, str_Wind_dir_angle, str_CGR3_TH_tempC, str_CGR3_LW_WM2 = format_converted_analog_to_str()
   str_outRH, str_outTemp, str_inRH, str_inTemp, str_pressure, str_mm_rain = format_digital_to_str()

   InputFile.write('\n'+columnSpacing.format(datetime, str_Apg_SW_WM2, str_inTemp, str_pressure, str_inRH, \
   str_mm_rain, str_Wind_dir_angle, 'nan', str_outTemp, str_outRH, str_CGR3_LW_WM2, str_CGR3_TH_tempC))

from os import system
def print_inputs():
   str_Apg_SW_WM2, str_Wind_dir_angle, str_CGR3_TH_tempC, str_CGR3_LW_WM2 = format_converted_analog_to_str()
   str_outRH, str_outTemp, str_inRH, str_inTemp, str_pressure, str_mm_rain = format_digital_to_str()
   datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime()) #get the current date and time

   print (sensorHeader+'\n'+measureHeader+'\n'+unitHeader)
   print('\n'+columnSpacing.format(datetime, str_Apg_SW_WM2, str_inTemp, str_pressure, str_inRH, \
   str_mm_rain, str_Wind_dir_angle, 'nan', str_outTemp, str_outRH, str_CGR3_LW_WM2, str_CGR3_TH_tempC))


def write_raw(): #Need to work on this
   datetime = time.strftime('%Y  %m  %d  %H  %M  %S', time.gmtime()) #get the current date and time
   str_CGR3_LW_V, str_CGR3_TH_V, str_Wind_dir_V, str_Apg_SW_V = format_raw_analog_to_str()
   str_outRH, str_outTemp, str_inRH, str_inTemp, str_pressure, str_mm_rain = format_digital_to_str()

   RawFile.write('\n'+columnSpacing.format(datetime, str_Apg_SW_V, str_inTemp, str_pressure, str_inRH, \
   str_mm_rain, str_Wind_dir_V, 'nan', str_outTemp, str_outRH, str_CGR3_LW_V, str_CGR3_TH_V))

def close():
        InputFile.close(); AvgFile.close()

from os import system
def upload():
        system('git add . && git commit -m weatherLog && git push')

