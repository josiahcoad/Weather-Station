import os
import plotly.plotly as py
import plotly.graph_objs as go

xysplit = fil.split('-')
os.system('clear')
#graph a list
chartname = raw_input('What would you like to call your chart? ') 
xdata = raw_input('Enter x data: ')
ydata = raw_input('Enter y data: ')
trace = go.Scatter(
        	x = xdata,
		y = ydata
	)	
py.iplot([trace], filename=chartname)
print 'Congrats! Now follow this link to see your plot: https://plot.ly/organize/home'
