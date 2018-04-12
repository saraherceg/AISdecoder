import gzip
import sys
import ais
import os
import time

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=80, llcrnrlon=-90, urcrnrlon=90, lat_ts=20, resolution='i')
map.drawcoastlines()
#map.shadedrelief()
map.drawparallels(np.arange(-90.,91.,30.))
map.drawmeridians(np.arange(-180.,181.,60.))
plt.title("Observations plot")

counter = 0

def plot_on_map(observation):
	global counter
	x = 0
	y = 0
	global map
	#print(observation)
	observation_list = observation.split(", ")
	for i in observation_list:
		if i.startswith("u'y'"):
			y_coordinate = i.split(": ")
			y = float(y_coordinate[1])
			#print y
		if i.startswith("u'x'"):
			x_coordinate = i.split(": ")
			x = float(x_coordinate[1])
			#print x
	if (x != 0 and y != 0): 
		lon, lat = map(x,y)
		map.plot(lon,lat,'ro', markersize = 2)
		plt.show()
		counter = counter + 1

start = time.time()

file = open('decoded.txt', 'r')
print ("plotting observations")
for line in file:
	plot_on_map(line)
	if (counter%1000 == 0):
		#print counter
		continue

end = time.time()
print("Time elapsed: " + str(end - start))
print("Plotted observations: " + str(counter))
plt.show()
