import gzip
import sys
import ais
import os
import time

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

decoded_observations = 0
all_observations = 0
MMSI = "367155310"

map = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, lat_ts=80, resolution='i')
map.drawcoastlines()
#map.shadedrelief()
map.drawparallels(np.arange(-90.,91.,30.))
map.drawmeridians(np.arange(-180.,181.,60.))
plt.title("One day observations")

def plot_on_map(observation):
	x = 0
	y = 0
	global map
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
	lon, lat = map(x,y)
	map.plot(lon,lat,'ro', markersize = 2)

def plot_route(observation):
	global counter
	global MMSI
	x = 0
	y = 0		
	found = False
	#field_name = "u'mmsi': 367155310"#+ MMSI
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
		if i.startswith("u'mmsi': 367509840"):
			found = True	
			print "found"	
	if (x != 0 and y != 0 and found):
		lon, lat = map(x,y)
		map.plot(lon,lat,'ro', markersize = 2)
		counter = counter + 1
		found = False



def decode(filename):

	file  = gzip.open(filename, 'r')
	output = open("out.txt", "a")

	global decoded_observations
	global all_observations
	timestamp = '0'

	for line in file:
		all_observations = all_observations +1
		try:
			line_list = line.split(",")

			field_0 = line_list[0]
			if(field_0[0] != "!"):
				# timestamp is present
				timestamp = field_0[:17]
			#data_1 = "'" + line_list[5] + "'"
			field_6 = line_list[6].rstrip('\r\n')
			if (str(field_6)[0] == "0"):
				decoded = str((ais.decode(str(line_list[5]), 0)))
				#print(decoded)
				## insert current timestamp value
				timestamp_position = (decoded).find("timestamp") + 12
				decoded_timestamp = decoded[:timestamp_position] + str(timestamp) + decoded[timestamp_position+3:]
			
	 			#output.write(decoded_timestamp+ '\n\n')
				if (all_observations%1 == 0):	#specify if want to only run through a part
					#print (all_observations)
					plot_route(decoded_timestamp)
					decoded_observations = decoded_observations+1	
			else:
				file.readline()      # skip next line as it is a part of previous observation
		except Exception:
			pass
	
	print ("Successfully decoded observations: " + str(decoded_observations) +"/" + str(all_observations) + " (" + str(float(decoded_observations)/float(all_observations)) + ")")	


print "hello"

start = time.time()

file_counter = 0
for filename in os.listdir(os.getcwd()):
	file_counter = file_counter+1
	print file_counter
	if filename.endswith(".txt.gz"):
		print ("decoding " + filename)
		decode(filename)
		continue
	else:
		continue

end = time.time()
print("Time elapsed: " + str(end - start))
plt.show()
