import csv
import re
import json
from collections import defaultdict

###############
# converting hospital data to json
###############

hospitals = {}

with open('hospital.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)

	next(csv_reader)

	for line in csv_reader:
		d = {}
		# d['name'] = line[1]
		# d['address'] = line[2]
		# d['city'] = line[3]
		# d['state'] = line[4]
		# d['zip'] = int(line[5])
		# d['county'] = line[6]
		# d['phone'] = int(line[7])
		# d['type'] = line[8]
		# d['ownership'] = line[9]
		# d['emergency'] = line[10]
		# d['ehr'] = line[11]
		d['rating'] = line[12]
		# d['rating_foot'] = line[13]
		d['mortality'] = line[14]
		# d['mortality_foot'] = line[15]
		d['safety'] = line[16]
		# d['safety_foot'] = line[17]
		# d['readmission'] = line[18]
		# d['readmission_foot'] = line[19]
		d['experience'] = line[20]
		# d['experience_foot'] = line[21]
		# d['care'] = line[22]
		# d['care_foot'] = line[23]
		# d['timeliness'] = line[24]
		# d['timeliness_foot'] = line[25]
		# d['imaging'] = line[26]
		# d['imaging_foot'] = line[27]
		r = re.findall(r'\d+.\d+, \-\d+.\d+', line[28])
		d['lat'] = ''
		d['long'] = ''
		if r:
			coord = r[0].split(",")
			d['lat'] = float(coord[0])
			d['long'] = float(coord[1])
		hospitals[int(line[0])] = d

# with open('hospital.json', 'w') as f:
# 	json.dump(hospitals, f)

###############
# converting us.json state name to abbreviated version
###############

# abbr = {}

# with open('state.csv', 'r') as csv_file:
# 	csv_reader = csv.reader(csv_file)

# 	next(csv_reader)

# 	for line in csv_reader:
# 		abbr[line[0]] = line[1]

# with open('us.json') as f:
# 	data = json.load(f)

# for state in data['objects']['states']['geometries']:
# 	name = str(state['properties']['name'])
# 	state['properties']['name'] = abbr[name]

# with open('us.json', 'w') as f:
# 	json.dump(data, f)


###############
# converting medicare data to json
###############

# medicare = {}

# with open('medicare.csv', 'r') as csv_file:
# 	csv_reader = csv.reader(csv_file)

# 	next(csv_reader)

# 	for line in csv_reader:
# 		if line[1] in hospitals:
# 			medicare[line[1]] = {}
# 			medicare[line[1]]['surgeries'] = {}
# 			d = {}
# 			d['discharge'] = int(line[8])
# 			d['avg_charge'] = float(line[9])
# 			d['avg_tot_pay'] = float(line[10])
# 			d['avg_med_pay'] = float(line[11])
# 			medicare[line[1]]['surgeries'][line[0]] = d

# with open('medicare.json', 'w') as f:
# 	json.dump(medicare, f)


###############
# avg surgery cost for state
###############

# num_per_state = defaultdict(int)
# state_covered = defaultdict(float)
# state_total = defaultdict(float)
# state_medicare = defaultdict(float)
# # state_cost = {}


# with open('medicare.csv', 'r') as csv_file:
# 	csv_reader = csv.reader(csv_file)

# 	next(csv_reader)

# 	for line in csv_reader:
# 		s = line[5]
# 		state_covered[s] += float(line[9])
# 		state_total[s] += float(line[10])
# 		state_medicare[s] += float(line[11])
# 		num_per_state[s] += 1

# for k in state_covered.keys():
# 	state_covered[k] /= num_per_state[k]
# 	state_total[k] /= num_per_state[k]
# 	state_medicare[k] /= num_per_state[k]

# print state_covered[max(state_covered.keys(), key=(lambda k: state_covered[k]))]
# print state_covered[min(state_covered.keys(), key=(lambda k: state_covered[k]))]

# print state_total[max(state_total.keys(), key=(lambda k: state_total[k]))]
# print state_total[min(state_total.keys(), key=(lambda k: state_total[k]))]

# print state_medicare[max(state_medicare.keys(), key=(lambda k: state_medicare[k]))]
# print state_medicare[min(state_medicare.keys(), key=(lambda k: state_medicare[k]))]

# state_cost['covered_charge'] = state_covered
# state_cost['total_pay'] = state_total
# state_cost['medicare_pay'] = state_medicare

# print state_cost

# with open('state_cost.json', 'w') as f:
# 	json.dump(state_covered, f)


###############
# add to geojson
###############

# with open('stateData.geojson') as f:
# 	data = json.load(f)

# for state in data['features']:
# 	name = state['properties']['name']
# 	a = abbr[name]
# 	state['properties']['avg_covered'] = state_covered[a]
# 	state['properties']['avg_tot_pay'] = state_total[a]
# 	state['properties']['avg_med_pay'] = state_medicare[a]


# with open('stateData.geojson', 'w') as f:
# 	json.dump(data, f)


###############
# medicare csv edit
###############

# medicare_processed = open('medicare_processed.csv', 'w')

# with open('medicare.csv', 'r') as csvfile:

# 	dataRows = csv.reader(csvfile, delimiter=',')
# 	for idx, line in enumerate(dataRows):
# 		outString = ""
# 		if idx == 0:
# 			for col in line:
# 				outString += col + ","
# 			outString += "latitude,longitude,rating,mortality,safety,experience"
# 			outString += "\n"
# 			medicare_processed.write(outString)
# 		else:
# 			if int(line[1]) in hospitals:
# 				d = hospitals[int(line[1])]

# 				if d['lat'] and d['long']:
# 					for col in line:
# 						outString += "\"" + col + "\"" + ","
					
# 					outString += str(d['lat']) + ',' + str(d['long']) + ',' + d['rating'] + ',' + d['mortality'] + ',' + d['safety'] + ',' + d['experience']
# 					outString += "\n"
# 					medicare_processed.write(outString)


###############
# medicare csv edit
###############

# # the template. where data from the csv will be formatted to geojson
# template = \
#    ''' \
#    { "type" : "Feature",
#        "geometry" : {
#            "type" : "Point",
#            "coordinates" : [%s, %s]},
#        "properties" : { "surgery" : "%s", "prov_id" : "%s", "name" : "%s", "avg_covered": %s, "avg_tot_pay": %s, "avg_med_pay": %s, "rating": "%s", "mortality": "%s", "safety": "%s", "experience": "%s"}
#        },
#    '''


# # the head of the geojson file
# output = \
#    ''' \

# { "type" : "FeatureCollection",
#    "features" : [
#    '''


# medicare_processed = open('medicare_processed.csv', 'w')

# s = set([001, 202, 293, 313, 536, 552, 652, 765, 864, 917])

# with open('medicare.csv', 'r') as csvfile:

# 	dataRows = csv.reader(csvfile, delimiter=',')
# 	for idx, line in enumerate(dataRows):
# 		if idx != 0:
# 			if int(line[1]) in hospitals:
# 				d = hospitals[int(line[1])]
# 				if d['long'] and d['lat'] and (int(line[0][:3]) in s):
# 					output += template % (d['long'], d['lat'], line[0], int(line[1]), line[2], line[9], line[10], line[11], d['rating'], d['mortality'], d['safety'], d['experience'])

# # the tail of the geojson file
# output += \
#    ''' \
#    ]

# }
#    '''

# # opens an geoJSON file to write the output
# outFileHandle = open("medicare_processed.geojson", "w")
# outFileHandle.write(output)
# outFileHandle.close()










