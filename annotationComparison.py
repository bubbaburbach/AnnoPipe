import re
import locEquiv
def Main(fileA,fileB,diffAllow):
#	import sys

######
    list1 = list()
    list2 = list()
    common = list()
    differences1 = list()
    differences2 = list()
    altList1 = list()
    altList2 = list()

    tempList = list()
#   debug = list()

    non_decimal = re.compile(r'[^\d.]')
#    template_rna = re.compile('  [trm]RNA  ')
    template_cds = re.compile('  CDS  ')
######
    altList1.append([])
    altList1.append([])
    altList2.append([])
    altList2.append([])    
#    print os.getcwd()
    with open(fileA) as handle:
        for item in handle:
#            if re.search(template_rna,item) or re.search(template_cds,item):
            if re.search(template_cds,item):
                list1.append(item.strip())
            if r'BASE COUNT' in item:
                break

    with open(fileB) as handle:
        for item in handle:
#            if re.search(template_rna,item) or re.search(template_cds,item):
            if re.search(template_cds,item):
                list2.append(item.strip())
            if r'//' in item:
                break
# grabs beginning and end positions of genes from gbk and prod files
# stores them in altList
    for item in list1:
        num = item.strip().replace(",","..").split("..")[-2]
        pole = non_decimal.sub('',num)
        altList1[0].append(pole[:])
        num = item.strip().replace(",","..").split("..")[-1]
        pole = non_decimal.sub('',num)
        altList1[1].append(pole[:])
        
    for item in list2:
        num = (item.strip().replace(",","..").split("..")[-2])
        pole1 = non_decimal.sub('',num)
        altList2[0].append(pole1[:])
        num = (item.strip().replace(",","..").split("..")[-1])
        pole1 = non_decimal.sub('',num)
        altList2[1].append(pole1[:])
        


#   Calculates the overlap difference between two annotated proteins.
#       If the ratio between the difference and the mean length of the two
#       proteins is less than the given cutoff, the two are declared 
#       equivalent and removed from their respective altList
#
#   Note: If genes are declared equivalent. Program takes representation
#       from fileA not fileB
#    while count1 < len(list1):
#        loc1 = [altList1[0][count1],altList1[1][count1]]
#        if altList1[0][count1] > altList1[1][count1]:
#            loc1 = [altList1[1][count1],altList1[0][count1]]    
#        while count2 < len(list2):
#            loc2 = [altList2[0][count2],altList2[1][count2]]
#            if altList2[0][count2] > altList2[1][count2]:
#                loc2 = [altList2[1][count2],altList2[0][count2]]
#            if loc2[1] == -1:
#                count2 = count2 + 1
#            elif (((abs(float(loc1[0])-float(loc2[0]))) + (abs(float(loc1[1])-float(loc2[1]))))/(((float(loc2[1])-float(loc2[0]))+(float(loc1[1])-float(loc1[0])))/2)) < diffAllow:
#                tempList.append(str(altList1[0][count1][:])+'..'+str(altList1[1][count1][:]))
#                altList1[0][count1] = -1
#                altList1[1][count1] = -1
#                altList2[0][count2] = -1
#                altList2[1][count2] = -1
#                break
#            else:
#                count2 = count2+1
#        count1 += 1
#        count2 = 0
#    print altList1[0]
    for index in locEquiv.equivIndices(altList1,altList2,diffAllow):
        common.append(list1[index])
#    for item in tempList:
#        for x in list1:
#            if item in x or 'complement('+item+')' in x:
#                common.append(x[:])
#    del tempList[:]
#    differences1.append(" Unique in " + fileA)
    tempList = [x for x in zip(altList1[0],altList1[1]) if x[0] != -1]
    for item in tempList:
        for x in list1:
            if " "+str(item[0])+".."+str(item[1])in x or "("+str(item[0])+".."+str(item[1])+')' in x:
                differences1.append(x[:])
    
    del tempList[:]
    tempList = [x for x in zip(altList2[0],altList2[1]) if x[0] != -1]
    for item in tempList:
        for x in list2:
            if " "+str(item[0])+".."+str(item[1]) in x or "("+str(item[0])+".."+str(item[1])+")" in x:
                differences2.append(x[:])
                
#    differences = differences1+differences2
    differences = [differences1,differences2]
    return(differences,common)
#
#	print "\n Common annotations"
#	for item in common:
#		for x in item:
#			print x
