import csv
import re
import operator




surgery_counts = open('surgery_counts.csv', 'w')

myDict = {}
			
with open('medicare.csv', 'r') as csvfile:

	dataRows = csv.reader(csvfile, delimiter=',')
	for idx, line in enumerate(dataRows):
		if idx != 0:
			surgeryName = line[0]
			if "W MCC" not in surgeryName and "W CC" not in surgeryName:
				if surgeryName not in myDict:
					myDict[surgeryName] = 1
				else:
					myDict[surgeryName] = myDict[surgeryName] + 1

	# Get list of surgeries by count
	sortedDictList = sorted(myDict.items(), key=operator.itemgetter(1))
	sortedDictList.reverse()


	# Trim above list to top i entries and remove count
	trimmedList = []
	for i in range(0, 100):
		trimmedList.append(sortedDictList[i][0])

	# Sort list
	sortedList = sorted(trimmedList)

	# Sorted list in the way that we want
	for line in sortedList:
		outString = "\"" + line + "\"," 
		print outString




	# Make accompanying pretty list




		

			
