import ais
import gzip
import datetime

#split signs
split_lines = '!'
split_time = ' '
split_message = ','
split_attribute = ': '
x = " u'x'"
y = " u'y'"

#global variables for data analysis
number_of_lines = 0
number_of_exceptions = 0


def decode_file(file_path, decoded_file):

	global number_of_exceptions
	global number_of_lines
	
	with gzip.open(file_path, 'rb') as f:
		for line in f:
			number_of_lines += 1
			try:
            #lines without time stamp
				if line.startswith(split_lines):
					decoded_file.write(str(ais.decode(line.split(split_message)[5], int(line.split(split_message)[6][:1])))+ '\n\n')
			#lines with time stamp
				else:
					list1 = line.split(split_time)
					decoded_file.write(str(datetime.datetime.fromtimestamp(float(list1[0]))) + '\n\n')
					try:
						decoded_file.write(str(ais.decode(line.split(split_message)[5], int(line.split(split_message)[6][:1])))+ '\n\n')
					
					#uncommon messages which start with time stamp
					except:
						number_of_exceptions += 1
						pass
		
			#uncommon messages
			except:
				number_of_exceptions += 1
				pass



decoded_message= open("decoded.txt", "w+")
decode_file('./ais-10-10/23-59.txt.gz', decoded_message)
print "number of exceptions: " + str(number_of_exceptions)
print "number of lines: " + str(number_of_lines)