#This code will read a file and seperate the data into individual indexes
#Based on the index position, the program knows what kind of data it is
#The user can choose what file he wants to graph and what type of data 
#It then will graph that data
import plotly.plotly as py
import plotly.graph_objs as go


step = 'haha'
x = 0
dataList = []
timeList = []

#Use user input to type in the data you want graphed and the file you want to use
#choosetype = raw_input ('Are you going to be graphing dataAvgs or dataInput? ')
#filename = raw_input ('Pick a file you would like graphed: ')
#print 'You chose:', choosetype + '/' + filename

#Open that file to read
#with open('%s/%s' % (choosetype, filename), 'r') as f:
with open('dataAvgs/2016-01-18 Hr:02', 'r') as f:
	str = f.read()

#Split the file into indexes using commas
comma_split = str.split(',')

#Choose the type of data to graph 
datatype = raw_input('What would you like to graph: light, temp, pressure or humidity ? ')

	
lineCount = len(comma_split) / 5
for x in range (lineCount):
	if datatype == 'light':
                step = x * 5 + 2
        elif datatype == 'temp':
                step = x * 5 + 3
        elif datatype == 'pressure':
                step = x * 5 + 4
        elif datatype == 'humidity':
                step = x * 5 + 5
	#saves those data points to a list
	data = (comma_split[step])
	dataList.append(data)
	print comma_split[step]
	#as the x axis, use the datetime
        datetime = (comma_split[x * 5 + 1])
	datetime = list(datetime)
	datetime = datetime[-10:-4]
	timeList.append(datetime)
#NEXT:
#graph that list
chartname = raw_input('What would you like to call your chart? ') 
trace = go.Scatter(
        	x = timeList,
		y = dataList
	)	
py.iplot([trace], filename=chartname)
#print 'Congrats! Now follow this link to see your plot: https://plot.ly/organize/home'


#P.S. What if the dataavgs got saved to a list and that list got graohed at the end. YES!
