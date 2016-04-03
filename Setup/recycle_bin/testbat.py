import sys; sys.path.insert(0, '/home/pi/Weather_Log/Setup/Sensors')
from ABEdiff_setup import ADCDifferentialPi
from ABEsmbus_setup import ABEHelpers
i2c_helper = ABEHelpers(); bus = i2c_helper.get_smbus()
ABEadc = ADCDifferentialPi(bus, 0x68, 0x69, 18)
import time
starttime = time.time()
file = open("Setup/Battery/batLog.txt","w")
voltage = 12
while voltage > 10:
   programtime = time.time()
   voltage = (ABEadc.read_voltage(1)*12.2)
   print "Voltage: %0.2f, Time: %0.0f" %(voltage, time.time()-starttime)
   file.write("%0.2f, %0.0f\n" %(voltage, time.time()-starttime))
   time.sleep(10-(time.time()-programtime))
file.write("\n\n\n\n\n\n\n")
file.close()
from os import system
system("sudo halt")

