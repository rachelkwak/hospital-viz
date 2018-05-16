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

medicare_processed = open('medicare_processed.csv', 'w')

with open('medicare.csv', 'r') as csvfile:

	dataRows = csv.reader(csvfile, delimiter=',')
	for idx, line in enumerate(dataRows):
		outString = ""
		if idx == 0:
			for col in line:
				outString += col + ","
			outString += "latitude,longitude,rating,mortality,safety,experience"
			outString += "\n"
			medicare_processed.write(outString)
		else:
			if int(line[1]) in hospitals:
				d = hospitals[int(line[1])]

				if d['lat'] and d['long']:
					for col in line:
						outString += "\"" + col + "\"" + ","
					
					outString += str(d['lat']) + ',' + str(d['long']) + ',' + d['rating'] + ',' + d['mortality'] + ',' + d['safety'] + ',' + d['experience']
					outString += "\n"
					medicare_processed.write(outString)


###############
# medicare csv edit
###############

# the template. where data from the csv will be formatted to geojson
template = \
   ''' \
   { "type" : "Feature",
       "geometry" : {
           "type" : "Point",
           "coordinates" : [%s, %s]},
       "properties" : { "surgery" : "%s", "prov_id" : "%s", "name" : "%s", "avg_covered": %s, "avg_tot_pay": %s, "avg_med_pay": %s, "rating": "%s", "mortality": "%s", "safety": "%s", "experience": "%s"}
       },
   '''


# the head of the geojson file
output = \
   ''' \

{ "type" : "FeatureCollection",
   "features" : [
   '''


medicare_processed = open('medicare_processed.csv', 'w')

s = set([
    "003 - ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R.",
	"004 - TRACH W MV 96+ HRS OR PDX EXC FACE, MOUTH & NECK W/O MAJ O.R.",
	"027 - CRANIOTOMY & ENDOVASCULAR INTRACRANIAL PROCEDURES W/O CC/MCC",
	"039 - EXTRACRANIAL PROCEDURES W/O CC/MCC",
	"057 - DEGENERATIVE NERVOUS SYSTEM DISORDERS W/O MCC",
	"066 - INTRACRANIAL HEMORRHAGE OR CEREBRAL INFARCTION W/O CC/MCC",
	"069 - TRANSIENT ISCHEMIA",
	"074 - CRANIAL & PERIPHERAL NERVE DISORDERS W/O MCC",
	"087 - TRAUMATIC STUPOR & COMA, COMA <1 HR W/O CC/MCC",
	"093 - OTHER DISORDERS OF NERVOUS SYSTEM W/O CC/MCC",
	"101 - SEIZURES W/O MCC",
	"103 - HEADACHES W/O MCC",
	"149 - DYSEQUILIBRIUM",
	"153 - OTITIS MEDIA & URI W/O MCC",
	"165 - MAJOR CHEST PROCEDURES W/O CC/MCC",
	"176 - PULMONARY EMBOLISM W/O MCC",
	"179 - RESPIRATORY INFECTIONS & INFLAMMATIONS W/O CC/MCC",
	"189 - PULMONARY EDEMA & RESPIRATORY FAILURE",
	"192 - CHRONIC OBSTRUCTIVE PULMONARY DISEASE W/O CC/MCC",
	"195 - SIMPLE PNEUMONIA & PLEURISY W/O CC/MCC",
	"203 - BRONCHITIS & ASTHMA W/O CC/MCC",
	"204 - RESPIRATORY SIGNS & SYMPTOMS",
	"206 - OTHER RESPIRATORY SYSTEM DIAGNOSES W/O MCC",
	"207 - RESPIRATORY SYSTEM DIAGNOSIS W VENTILATOR SUPPORT 96+ HOURS",
	"208 - RESPIRATORY SYSTEM DIAGNOSIS W VENTILATOR SUPPORT <96 HOURS",
	"221 - CARDIAC VALVE & OTH MAJ CARDIOTHORACIC PROC W/O CARD CATH W/O CC/MCC",
	"227 - CARDIAC DEFIBRILLATOR IMPLANT W/O CARDIAC CATH W/O MCC",
	"234 - CORONARY BYPASS W CARDIAC CATH W/O MCC",
	"236 - CORONARY BYPASS W/O CARDIAC CATH W/O MCC",
	"238 - MAJOR CARDIOVASC PROCEDURES W/O MCC",
	"244 - PERMANENT CARDIAC PACEMAKER IMPLANT W/O CC/MCC",
	"247 - PERC CARDIOVASC PROC W DRUG-ELUTING STENT W/O MCC",
	"249 - PERC CARDIOVASC PROC W NON-DRUG-ELUTING STENT W/O MCC",
	"251 - PERC CARDIOVASC PROC W/O CORONARY ARTERY STENT W/O MCC",
	"254 - OTHER VASCULAR PROCEDURES W/O CC/MCC",
	"264 - OTHER CIRCULATORY SYSTEM O.R. PROCEDURES",
	"267 - ENDOVASCULAR CARDIAC VALVE REPLACEMENT W/O MCC",
	"282 - ACUTE MYOCARDIAL INFARCTION, DISCHARGED ALIVE W/O CC/MCC",
	"287 - CIRCULATORY DISORDERS EXCEPT AMI, W CARD CATH W/O MCC",
	"293 - HEART FAILURE & SHOCK W/O CC/MCC",
	"301 - PERIPHERAL VASCULAR DISORDERS W/O CC/MCC",
	"303 - ATHEROSCLEROSIS W/O MCC",
	"305 - HYPERTENSION W/O MCC",
	"310 - CARDIAC ARRHYTHMIA & CONDUCTION DISORDERS W/O CC/MCC",
	"312 - SYNCOPE & COLLAPSE",
	"313 - CHEST PAIN",
	"328 - STOMACH, ESOPHAGEAL & DUODENAL PROC W/O CC/MCC",
	"331 - MAJOR SMALL & LARGE BOWEL PROCEDURES W/O CC/MCC",
	"355 - HERNIA PROCEDURES EXCEPT INGUINAL & FEMORAL W/O CC/MCC",
	"373 - MAJOR GASTROINTESTINAL DISORDERS & PERITONEAL INFECTIONS W/O CC/MCC",
	"379 - G.I. HEMORRHAGE W/O CC/MCC",
	"390 - G.I. OBSTRUCTION W/O CC/MCC",
	"392 - ESOPHAGITIS, GASTROENT & MISC DIGEST DISORDERS W/O MCC",
	"395 - OTHER DIGESTIVE SYSTEM DIAGNOSES W/O CC/MCC",
	"419 - LAPAROSCOPIC CHOLECYSTECTOMY W/O C.D.E. W/O CC/MCC",
	"440 - DISORDERS OF PANCREAS EXCEPT MALIGNANCY W/O CC/MCC",
	"446 - DISORDERS OF THE BILIARY TRACT W/O CC/MCC",
	"455 - COMBINED ANTERIOR/POSTERIOR SPINAL FUSION W/O CC/MCC",
	"460 - SPINAL FUSION EXCEPT CERVICAL W/O MCC",
	"462 - BILATERAL OR MULTIPLE MAJOR JOINT PROCS OF LOWER EXTREMITY W/O MCC",
	"468 - REVISION OF HIP OR KNEE REPLACEMENT W/O CC/MCC",
	"470 - MAJOR JOINT REPLACEMENT OR REATTACHMENT OF LOWER EXTREMITY W/O MCC",
	"473 - CERVICAL SPINAL FUSION W/O CC/MCC",
	"482 - HIP & FEMUR PROCEDURES EXCEPT MAJOR JOINT W/O CC/MCC",
	"483 - MAJOR JOINT/LIMB REATTACHMENT PROCEDURE OF UPPER EXTREMITIES",
	"494 - LOWER EXTREM & HUMER PROC EXCEPT HIP,FOOT,FEMUR W/O CC/MCC",
	"517 - OTHER MUSCULOSKELET SYS & CONN TISS O.R. PROC W/O CC/MCC",
	"520 - BACK & NECK PROC EXC SPINAL FUSION W/O CC/MCC",
	"536 - FRACTURES OF HIP & PELVIS W/O MCC",
	"552 - MEDICAL BACK PROBLEMS W/O MCC",
	"554 - BONE DISEASES & ARTHROPATHIES W/O MCC",
	"556 - SIGNS & SYMPTOMS OF MUSCULOSKELETAL SYSTEM & CONN TISSUE W/O MCC",
	"558 - TENDONITIS, MYOSITIS & BURSITIS W/O MCC",
	"563 - FX, SPRN, STRN & DISL EXCEPT FEMUR, HIP, PELVIS & THIGH W/O MCC",
	"603 - CELLULITIS W/O MCC",
	"605 - TRAUMA TO THE SKIN, SUBCUT TISS & BREAST W/O MCC",
	"621 - O.R. PROCEDURES FOR OBESITY W/O CC/MCC",
	"639 - DIABETES W/O CC/MCC",
	"641 - MISC DISORDERS OF NUTRITION,METABOLISM,FLUIDS/ELECTROLYTES W/O MCC",
	"652 - KIDNEY TRANSPLANT",
	"658 - KIDNEY & URETER PROCEDURES FOR NEOPLASM W/O CC/MCC",
	"684 - RENAL FAILURE W/O CC/MCC",
	"690 - KIDNEY & URINARY TRACT INFECTIONS W/O MCC",
	"694 - URINARY STONES W/O ESW LITHOTRIPSY W/O MCC",
	"696 - KIDNEY & URINARY TRACT SIGNS & SYMPTOMS W/O MCC",
	"708 - MAJOR MALE PELVIC PROCEDURES W/O CC/MCC",
	"743 - UTERINE & ADNEXA PROC FOR NON-MALIGNANCY W/O CC/MCC",
	"812 - RED BLOOD CELL DISORDERS W/O MCC",
	"813 - COAGULATION DISORDERS",
	"863 - POSTOPERATIVE & POST-TRAUMATIC INFECTIONS W/O MCC",
	"864 - FEVER",
	"870 - SEPTICEMIA OR SEVERE SEPSIS W MV >96 HOURS",
	"872 - SEPTICEMIA OR SEVERE SEPSIS W/O MV >96 HOURS W/O MCC",
	"881 - DEPRESSIVE NEUROSES",
	"884 - ORGANIC DISTURBANCES & MENTAL RETARDATION",
	"885 - PSYCHOSES",
	"894 - ALCOHOL/DRUG ABUSE OR DEPENDENCE, LEFT AMA",
	"897 - ALCOHOL/DRUG ABUSE OR DEPENDENCE W/O REHABILITATION THERAPY W/O MCC",
	"918 - POISONING & TOXIC EFFECTS OF DRUGS W/O MCC",
	"948 - SIGNS & SYMPTOMS W/O MCC"
])

with open('medicare.csv', 'r') as csvfile:

	dataRows = csv.reader(csvfile, delimiter=',')
	for idx, line in enumerate(dataRows):
		if idx != 0:
			if int(line[1]) in hospitals:
				d = hospitals[int(line[1])]
				if d['long'] and d['lat'] and line[0] in s:
					output += template % (d['long'], d['lat'], line[0], int(line[1]), line[2], line[9], line[10], line[11], d['rating'], d['mortality'], d['safety'], d['experience'])

# the tail of the geojson file
output += \
   ''' \
   ]

}
   '''

# opens an geoJSON file to write the output
outFileHandle = open("medicare_processed.geojson", "w")
outFileHandle.write(output)
outFileHandle.close()










