import numpy as np

id = " u'mmsi'"
split_message = ','
split_attribute = ': '

id_list = []

with open('decoded.txt','r') as decoded:
    for line in decoded:
		attribute_list = line.split(split_message)
		if line.startswith("20"): #timestamp
			pass
				
		else:
			for attribute in attribute_list:
				if attribute.startswith(id):
					id_1 = attribute.split(split_attribute)
					ship_id = id_1[1]
					ship_id = ship_id[:-1]
					id_list.append(ship_id)
				else:
					pass
		
					
					
numpyarray = np.array(id_list)
a = np.unique(numpyarray)
print len(a)

#write the numpy array to a file (only for debugging):
# with open('ids.txt','w') as ids:
	# ids.write(a)
