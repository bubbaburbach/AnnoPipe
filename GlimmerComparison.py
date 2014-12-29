import string
import re
import os
import locEquiv

    
def Main(inList,glimm,diffAllow):
#	import argparse


#	parser = argparse.ArgumentParser(description='Compare output of annotationComparison.py with the output of Glimmer')
#	parser.add_argument('-i','--infile',type=str,help="The difference file from annotationComparison.py",required=True,dest='infile')
#	parser.add_argument('-g','--glimm',type=str,help="The .predict file from Glimmer",required=True,dest='glimm')
#	parser.add_argument('-o','--out',type=str,help="The output file for the program",default='out.txt',required=True,dest='out')

#	args = parser.parse_args()
    glimList = list()
#    origList = list()
#    geneList = list()
    altList1 = list()
    altList2 = list()
#    list_temp = list()
    list_gbk = list()
    list_prod = list()

#    commonList = list()
#    commonFlag = False
    non_decimal = re.compile(r'[^\d.]+')
    altList1.append([])
    altList1.append([])
    altList2.append([])
    altList2.append([])
#	with open(args.infile,"r") as origFile:
#    for item in inList:
#        if "Common" in item:
#            commonFlag = True
#        if commonFlag:
#            commonList.append(item)
#        elif item != "\n":
#            origList.append(item)
    
    if not os.path.isfile(glimm):
        temp = glimm.split(".")
        glimm = ".run1.".join(temp)
    
    if os.path.isfile(glimm):
        with open(glimm,"r") as glimFile:
            for item in glimFile:
                if "orf" in item:
                    focus = item.split()
                    focus[1] = non_decimal.sub('',focus[1])
                    focus[2] = non_decimal.sub('',focus[2])
                    altList2[0].append(int(focus[1]))
                    altList2[1].append(int(focus[2]))
                    glimList.append((int(focus[1]),int(focus[2])))

                
        for item in inList[0]:
            if item != ' ':
                focus = re.split('[().]',item.translate(None,string.ascii_letters).translate(None,"()").strip())
                altList1[0].append(int(non_decimal.sub('',focus[0])))
                altList1[1].append(int(non_decimal.sub('',focus[2])))

#        count1 = 0
#        count2 = 0                
#        while count1 < len(inList[0]):
#            loc1 = [altList1[0][count1],altList1[1][count1]]
#            if altList1[0][count1] > altList1[1][count1]:
#                loc1 = [altList1[1][count1],altList1[0][count1]]    
#            while count2 < len(glimList):
#                loc2 = [altList2[0][count2],altList2[1][count2]]
#                if altList2[0][count2] > altList2[1][count2]:
#                    loc2 = [altList2[1][count2],altList2[0][count2]]
#                if loc2[1] == -1:
#                    count2 = count2 + 1
#                elif (((abs(float(loc1[0])-float(loc2[0]))) + (abs(float(loc1[1])-float(loc2[1]))))/(((float(loc2[1])-float(loc2[0]))+(float(loc1[1])-float(loc1[0])))/2)) < diffAllow:
##                    list_temp.append(str(altList1[0][count1][:])+'..'+str(altList1[1][count1][:]))
#                    list_gbk.append(inList[0][count1])
#                    altList1[0][count1] = -1
#                    altList1[1][count1] = -1
#                    altList2[0][count2] = -1
#                    altList2[1][count2] = -1
#                    break
#                else:
#                    count2 = count2+1
#            count1 += 1
#            count2 = 0
        for index in locEquiv.equivIndices(altList1,altList2,diffAllow):
            list_gbk.append(inList[0][index])
            
        del(altList1[0][:])
        del(altList1[1][:])
        for item in inList[1]:
            if item != ' ':
                focus = re.split('[().]',item.translate(None,string.ascii_letters).translate(None,"()").strip())
                altList1[0].append(int(non_decimal.sub('',focus[0])))
                altList1[1].append(int(non_decimal.sub('',focus[2])))
                
#        count1 = 0
#        count2 = 0                
#        while count1 < len(inList[1]):
#            loc1 = [altList1[0][count1],altList1[1][count1]]
#            if altList1[0][count1] > altList1[1][count1]:
#                loc1 = [altList1[1][count1],altList1[0][count1]]
#            while count2 < len(glimList):
#                loc2 = [altList2[0][count1],altList2[1][count1]]
#                if altList2[0][count2] > altList2[1][count2]:
#                    loc2 = [altList2[1][count1],altList2[0][count1]]
#                if loc2[1] == -1:
#                    count2 = count2 + 1
#                elif (((abs(float(loc1[0])-float(loc2[0]))) + (abs(float(loc1[1])-float(loc2[1]))))/(((float(loc2[1])-float(loc2[0]))+(float(loc1[1])-float(loc1[0])))/2)) < diffAllow:
##                    list_temp.append(str(altList1[0][count1][:])+'..'+str(altList1[1][count1][:]))
#                    list_prod.append(inList[1][count1])
#                    altList1[0][count1] = -1
#                    altList1[1][count1] = -1
#                    altList2[0][count2] = -1
#                    altList2[1][count2] = -1
#                    break
#                else:
#                    count2 = count2+1
#            count1 += 1
#            count2 = 0
        for index in locEquiv.equivIndices(altList1,altList2,diffAllow):
            list_prod.append(inList[1][index])
#        for item in origList:
#            count = count+1
#            if 'Unique' in item:
#                geneList.append(item)
#            elif item != ' ':
#                focus = re.split('[().]',item.translate(None,string.ascii_letters).translate(None,"()").strip())
#                focus[0] = non_decimal.sub('',focus[0])
#                focus[2] = non_decimal.sub('',focus[2])
#                if int(focus[0]) < int(focus[2]):
#                    if (int(focus[0]),int(focus[2])) in glimSet:
#                        geneList.append(item)
#                elif (int(focus[2]),int(focus[0])) in glimSet:
#                    geneList.append(item)
    else:
        print "Glimm file not found"
                    
#    for item in commonList:
#        geneList.append(item)
    print '\nGlimmer confirmed '+str(len(list_gbk))+' of '+str(len(inList[0]))+' mismatches from rast'
    print 'Glimmer confirmed '+str(len(list_prod))+' of '+str(len(inList[1]))+' mismatches from prodigal\n'
    return(list_gbk,list_prod)
#	with open(args.out,"w") as handle:
#		for item in geneList:
#			handle.write(item)
#		handle.write("\n")
#		for item in commonList:
#			handle.write(item)
