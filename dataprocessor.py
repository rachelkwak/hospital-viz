import csv
import re

# Start

hospitals_processed = open('hospitals_processed.csv', 'w')

# Go through dataset once first to find median values
with open('hospital.csv', 'r') as csvfile:

	dataRows = csv.reader(csvfile, delimiter=',')
	for idx, line in enumerate(dataRows):
		outString = ""
		if idx == 0:
			for i in range(len(line)):
				outString += line[i] + ","
			outString += "latitude,longitude"
			outString += "\n"
			hospitals_processed.write(outString)
		else:
			r = re.findall(r'\d+.\d+, \-\d+.\d+', line[28])
			if r:
				coord = r[0].split(",")
				latitude = str(float(coord[0]))
				longitude = str(float(coord[1]))

				for i in range(len(line)):
					outString += "\"" + line[i] + "\"" + ","
				
				outString += latitude + ',' + longitude
				outString += "\n"
				hospitals_processed.write(outString)

			
