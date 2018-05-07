import csv
import re






# hospitals_processed = open('hospitals_processed.csv', 'w')

# with open('hospital.csv', 'r') as csvfile:

# 	dataRows = csv.reader(csvfile, delimiter=',')
# 	for idx, line in enumerate(dataRows):
# 		outString = ""
# 		if idx == 0:
# 			for i in range(len(line)):
# 				outString += line[i] + ","
# 			outString += "latitude,longitude"
# 			outString += "\n"
# 			hospitals_processed.write(outString)
# 		else:
# 			r = re.findall(r'\d+.\d+, \-\d+.\d+', line[28])
# 			if r:
# 				coord = r[0].split(",")
# 				latitude = str(float(coord[0]))
# 				longitude = str(float(coord[1]))

# 				for i in range(len(line)):
# 					outString += "\"" + line[i] + "\"" + ","
				
# 				outString += latitude + ',' + longitude
# 				outString += "\n"
# 				hospitals_processed.write(outString)







states = [
	"AL",
	"AK",
	"AZ",
	"AR",
	"CA",
	"CO",
	"CT",
	"DE",
	"FL",
	"GA",
	"HI",
	"ID",
	"IL",
	"IN",
	"IA",
	"KS",
	"KY",
	"LA",
	"ME",
	"MD",
	"MA",
	"MI",
	"MN",
	"MS",
	"MO",
	"MT",
	"NE",
	"NV",
	"NH",
	"NJ",
	"NM",
	"NY",
	"NC",
	"ND",
	"OH",
	"OK",
	"OR",
	"PA",
	"RI",
	"SC",
	"SD",
	"TN",
	"TX",
	"UT",
	"VT",
	"VA",
	"WA",
	"WV",
	"WI",
	"WY",
	"DC"
]

surgeries = [
	"001 - HEART TRANSPLANT OR IMPLANT OF HEART ASSIST SYSTEM W MCC",
	"202 - BRONCHITIS & ASTHMA W CC/MCC",
	"293 - HEART FAILURE & SHOCK W/O CC/MCC",
	"313 - CHEST PAIN",
	"536 - FRACTURES OF HIP & PELVIS W/O MCC",
	"552 - MEDICAL BACK PROBLEMS W/O MCC",
	"652 - KIDNEY TRANSPLANT",
	"765 - CESAREAN SECTION W CC/MCC",
	"864 - FEVER",
	"917 - POISONING & TOXIC EFFECTS OF DRUGS W MCC"
]

myDict = {}

surgery_state_averages = open('surgery_state_averages.csv', 'w')

for state in states:
	for surgery in surgeries:
		myDict[state + " " + surgery] = []
			
with open('medicare.csv', 'r') as csvfile:

	dataRows = csv.reader(csvfile, delimiter=',')
	for idx, line in enumerate(dataRows):
		if idx != 0:
			if line[5] + " " + line[0] in myDict:
				myDict[line[5] + " " + line[0]].append(float(line[10]))

	for key in myDict:
		if len(myDict[key]) != 0:
			average = sum(myDict[key])/len(myDict[key])
			myDict[key] = average
		else:
			myDict[key] = 0
			#myDict.pop(key, None)

	surgery_state_averages.write("Surgery,State,Cost\n")

	for key in myDict:
		outString = ""
		outString = ""
		keyString = key.partition(" ")
		state = keyString[0]
		surgery = keyString[2]
		print state
		print surgery
		surgery_state_averages.write(surgery + "," + state + "," + str(myDict[key]) + "\n")

		

			
