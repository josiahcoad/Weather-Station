# Remote Weather Logger Using Raspberry Pi

### Sensors Used:
-BME280
  -inRH, inTemp, pressure
-HYT221
  -outRH, outTemp
-ADS1115 (Analog Digital Converter)
  -Rain Gauge (on channel 0)
-ABE Differential (ADC)
  -CGR3
    -Temperature(8)
    -Long Wave Radiation(7)
  -Wind
    -Wind Direction (6)
    -Wind Speed (5) *Still working on this one
  -Apogee
    -Short Wave Radiation(4)

### How the Rain Gauge Works
The ADC has an alert pin which can be toggled if a designated channel goes high
Set channel where the rain bucket will be plugged into the ADS1115
Set GPIO pin where the pi will read the value of the toggle
And make sure to start_toggle_watch(channel) at the beginning of the Main code

### Wiring Hook-ups
Apogee	|Sensor	|Connector
_________________________________
A0	|Green	> Red
3.3V	|White	> Blu
GND	|Clear	> Ylw

Wind  		|Sensor |Connector
_________________________________
3.3V		|White	>  
Speed Sig	|Red	>
Speed Gnd	|Blue	>
Direction Sig	|Green	>
Direction Sig	|Black	>

CGR3		|Sensor	|Connector
_________________________________
GND (THERM)	|Green	> White
V-OUT (THERM)	|Yellow	> Yellow
GND (PYRO)	|Blue	> Black
V-OUT (PYRO)	|Red	> Red
_________________________________
BME280
3vol > 3v3      
GND > GND       
SCK > SCL       
SDI > SDA       
