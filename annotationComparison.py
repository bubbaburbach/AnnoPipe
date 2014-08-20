import re
def Main(fileA,fileB):
#	import sys

######
    list1 = list()
    list2 = list()
    common = list()
    differences1 = list()
    differences2 = list()
    altList1 = list()
    altList2 = list()
    count1 = 0
    count2 = 0
    diffAllow = .1
    tempList = list()
#   debug = list()

    non_decimal = re.compile(r'[^\d.]')
    
######
    altList1.append([])
    altList1.append([])
    altList2.append([])
    altList2.append([])
    
#    print os.getcwd()
    with open(fileA) as handle:
        for item in handle:
            if "  CDS  " in item or "  tRNA  " in item:
                list1.append(item.strip())

    with open(fileB) as handle:
        for item in handle:
            if "  CDS  " in item or "  tRNA  " in item:
                list2.append(item.strip())
    
    for item in list1:
        num = (item.strip().replace(",","..").split("..")[-2])
        pole = non_decimal.sub('',num)
        altList1[0].append(pole)
        num = (item.strip().replace(",","..").split("..")[-1])
        pole = non_decimal.sub('',num)
        altList1[1].append(pole)
        
    for item in list2:
        num = (item.strip().replace(",","..").split("..")[-2])
        pole = non_decimal.sub('',num)
        altList2[0].append(pole)
        num = (item.strip().replace(",","..").split("..")[-1])
        pole = non_decimal.sub('',num)
        altList2[1].append(pole)
        

    while count1 < len(list1):
        while count2 < len(list2):
            if altList2[0][count2] == 0:
                count2 = count2 + 1
            elif (((abs(float(altList1[0][count1])-float(altList2[0][count2]))) + (abs(float(altList1[1][count1])-float(altList2[1][count2]))))/(((float(altList2[1][count2])-float(altList2[0][count2]))+(float(altList1[1][count1])-float(altList1[0][count1])))/2)) < diffAllow:
                tempList.append(altList1[0][count1][:])
                altList1[0][count1] = 0
                altList1[1][count1] = 0
                altList2[0][count2] = 0
                altList2[1][count2] = 0
                break
            else:
                count2 = count2+1
        count1 += 1
        count2 = 0
        
    for item in tempList:
        for x in list1:
            if " "+str(item)+".." in x or "("+str(item)+".." in x or ","+str(item)+".." in x:
                common.append(x[:])
  
    del tempList[:]
    differences1.append(" Unique in " + fileA)
    tempList = [x for x in altList1[0] if x != 0]
    for item in tempList:
        for x in list1:
            if " "+str(item)+".." in x or "("+str(item)+".." in x or ","+str(item)+".." in x:
                differences1.append(x[:])
    
    del tempList[:]
    differences2.append("	Unique in " + fileB)
    tempList = [x for x in altList2[0] if x != 0]
    for item in tempList:
        for x in list2:
            if " "+str(item)+".." in x or "("+str(item)+".." in x or ","+str(item)+".." in x:
                differences2.append(x[:])
    
#    differences.append("	Unique in " + fileA)
 #   tempList = [x for x in list1 if x not in list2]
  #  for item in tempList:
 #        differences.append(item)
#    differences.append(" ")
 #   differences.append("	Unique in " + fileB)
  #  tempList = [x for x in list2 if x not in list1]
 #   for item in tempList:
#        differences.append(item)
 #   common.append([x for x in list1 if x in list2])
#
    differences = differences1+differences2
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
