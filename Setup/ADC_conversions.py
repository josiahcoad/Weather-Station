'''
================================================
Meterological Research Station - Dr. Ayal Anis
Created by Josiah Coad
ADC_convertions.py - version 1.0 - 10/23/2016

PURPOSE:This library can be used by the sensor_process library 
	to convert analog values to respective units

Conversion included: 
-Wind:   Angle
-Apogee: W/M^2
-CGR3:   tempC
-        tempC to tempK 
-CGR3:   W/M^2   
================================================
'''

from numpy import log

def V_to_angle(V):
   angle = V*400.00
   return angle 

def Apogee_V_to_WM2(V):
	WM2 = 5000 * V
	return WM2

def CGR3_V_to_tempC(V):
   global tempC
   R = (V/(3.324-V))*15000.0
   a = 1.0295 * 10**-3 
   b = 2.391 * 10**-4
   c = 1.568 * 10**-7
   tempC = ((a+(b*(log(R))+c*(log(R))**3))**-1) - 273.15
   return tempC

def CGR3_V_to_WM2(V):
   tempK = tempC + 273.15
   #CGR3_V_to_tempC(V)
   c=5.67*10**-8
   WM2= ((V*10**6)/10) + c * tempK**4
   return WM2
