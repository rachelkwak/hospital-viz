import csv
import re
import json
from collections import defaultdict

###############
# converting hospital data to json
###############

# hospitals = []

# with open('hospital.csv', 'r') as csv_file:
# 	csv_reader = csv.reader(csv_file)

# 	next(csv_reader)

# 	for line in csv_reader:
# 		d = {}
# 		d['id'] = line[0]
# 		d['name'] = line[1]
# 		d['address'] = line[2]
# 		d['city'] = line[3]
# 		d['state'] = line[4]
# 		d['zip'] = int(line[5])
# 		d['county'] = line[6]
# 		d['phone'] = int(line[7])
# 		d['type'] = line[8]
# 		d['ownership'] = line[9]
# 		d['emergency'] = line[10]
# 		d['ehr'] = line[11]
# 		d['rating'] = line[12]
# 		d['rating_foot'] = line[13]
# 		d['mortality'] = line[14]
# 		d['mortality_foot'] = line[15]
# 		d['safety'] = line[16]
# 		d['safety_foot'] = line[17]
# 		d['readmission'] = line[18]
# 		d['readmission_foot'] = line[19]
# 		d['experience'] = line[20]
# 		d['experience_foot'] = line[21]
# 		d['care'] = line[22]
# 		d['care_foot'] = line[23]
# 		d['timeliness'] = line[24]
# 		d['timeliness_foot'] = line[25]
# 		d['imaging'] = line[26]
# 		d['imaging_foot'] = line[27]
# 		r = re.findall(r'\d+.\d+, \-\d+.\d+', line[28])
# 		d['lat'] = ''
# 		d['long'] = ''
# 		if r:
# 			coord = r[0].split(",")
# 			d['lat'] = float(coord[0])
# 			d['long'] = float(coord[1])
# 		hospitals.append(d)

# with open('hospital.json', 'w') as f:
# 	json.dump(hospitals, f)

###############
# converting us.json state name to abbreviated version
###############

abbr = {}

with open('state.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)

	next(csv_reader)

	for line in csv_reader:
		abbr[line[0]] = line[1]

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

num_per_state = defaultdict(int)
state_covered = defaultdict(float)
state_total = defaultdict(float)
state_medicare = defaultdict(float)
# state_cost = {}


with open('medicare.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)

	next(csv_reader)

	for line in csv_reader:
		s = line[5]
		state_covered[s] += float(line[9])
		state_total[s] += float(line[10])
		state_medicare[s] += float(line[11])
		num_per_state[s] += 1

for k in state_covered.keys():
	state_covered[k] /= num_per_state[k]
	state_total[k] /= num_per_state[k]
	state_medicare[k] /= num_per_state[k]

# state_cost['covered_charge'] = state_covered
# state_cost['total_pay'] = state_total
# state_cost['medicare_pay'] = state_medicare

# print state_cost

# with open('state_cost.json', 'w') as f:
# 	json.dump(state_covered, f)


###############
# add to geojson
###############

with open('stateData.geojson') as f:
	data = json.load(f)

for state in data['features']:
	name = state['properties']['name']
	a = abbr[name]
	state['properties']['avg_covered'] = state_covered[a]
	state['properties']['avg_tot_pay'] = state_total[a]
	state['properties']['avg_med_pay'] = state_medicare[a]


with open('stateData.geojson', 'w') as f:
	json.dump(data, f)






















