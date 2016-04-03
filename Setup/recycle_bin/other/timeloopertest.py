from time import sleep
hours = int(raw_input("How many hours to simulate: "))
startmin = int(raw_input("Min to start on: "))
userMin = int(raw_input("Mins between logs: "))
currentMin = startmin
prevMin = currentMin
runs = 0
if currentMin = prevMin + 5
	print "code ran"


'''-
for x in range (hours):
	if x != 0:
		startmin = 0	
	for currentMin in range (startmin, 60):
		if prevMin + userMin > 59:
			prevMin = 59 - prevMin 
		if currentMin == prevMin + userMin:
			print runs, "minutes averaged"
			runs = 0
			prevMin = currentMin
		runs += 1
		#print 'currentMin', currentMin, 'prevMin', prevMin, 'userMin', userMin
		#sleep(.01)
-'''
