def Main(fileA,fileB):
#	import sys
	import string

	list1 = list()
	list2 = list()
	common = list()
	differences = list()

	with open(fileA) as handle:
		for item in handle:
			if "  CDS  " in item or "  tRNA  " in item:
				list1.append(item.strip())

	with open(fileB) as handle:
		for item in handle:
			if "  CDS  " in item or "  tRNA  " in item:
				list2.append(item.strip())
	
	differences.append("	Unique in " + fileA)
	tempList = [x for x in list1 if x not in list2]
	for item in tempList:
		differences.append(item)
	differences.append(" ")
	differences.append("	Unique in " + fileB)
	tempList = [x for x in list2 if x not in list1]
	for item in tempList:
		differences.append(item)
	common.append([x for x in list1 if x in list2])

	return(differences,common)
#	for item in differences:
#		if item is not string:
#			for x in item:
#				print x
#		else:
#			print item
#
#	print "\n Common annotations"
#	for item in common:
#		for x in item:
#			print x
