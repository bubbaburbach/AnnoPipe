# -*- coding: utf-8 -*-
import re

cds_template = re.compile("  CDS  ")
rna_template = re.compile("  [trm]RNA  ")
non_decimal = re.compile(r'[^\d.]+')

id_default = [cds_template,rna_template]#,gene_template]

def findPoles(listA):
    altList1 = [[],[]]
    for item in listA:
        num = item.strip().replace(",","..").split("..")[0]
        pole = non_decimal.sub('',num)
        altList1[0].append(int(pole[:]))
        num2 = item.strip().replace(",","..").split("..")[-1]
        pole = non_decimal.sub('',num2)
        altList1[1].append(int(pole[:]))       
    return altList1
    
def sortPoles(altList1,altList2):
    #sorting poles so it always reads '(low,high)'
    t = 0
    while t < len(altList1[0]):
        if altList1[0][t] > altList1[1][t]:
            a = altList1[0][t]
            altList1[0][t] = altList1[1][t]
            altList1[1][t] = a
        t = t+1
        
    t = 0
    while t < len(altList2[0]):
        if altList2[0][t] > altList2[1][t]:
            a = altList2[0][t]
            altList2[0][t] = altList2[1][t]
            altList2[1][t] = a
        t = t+1
        
    return altList1,altList2

def grabLocs(fileA,identifiers=id_default):
    inListA = list()
    with open(fileA) as focus:
        for item in focus:
            for xx in identifiers:
                if re.search(xx,item):
                    inListA.append(item)
    return(inListA)
        
def getAltLists(fileA,fileB,identifiers=id_default):
# creates a list of sets of start and end locations for gene sites
# e.g. 
# 1..2, 3..4,5..6 becomes
#[[1,3,5][2,4,6]]
# used in location comparisons
# 
    inListA = grabLocs(fileA,identifiers)
    inListB = grabLocs(fileB,identifiers)
    altList1=findPoles(inListA)        
    altList2=findPoles(inListB)
    return sortPoles(altList1,altList2)
    
def genesFromSet(fileA,setA,identifiers=id_default,offal=[]):
# give a set of paired (start,end)/(end,start) locations pulls the annotation
# from the given file
# also returns number of items from the set that were not found in the file
    annList = list()
    tempList = list()
    inList = list()
    keepFlag = False
    switchFlag = False
    firstPass = True
    with open(fileA) as focus:
        for line in focus:
            #majority of files are genbank so this was left in
            if 'BASE COUNT' in line:
                break
            else:
                inList.append(line) 
    count = 0
#    print "gfset inList: "+str(len(inList))
#    print "gfset setA: "+str(len(setA))
    for item in inList:
        for xx in identifiers:
            if re.search(xx,item):
                alpha = int(non_decimal.sub('',item.strip().replace(",","..").split('..')[0]))
                beta = int(non_decimal.sub('',item.strip().replace(",","..").split('..')[-1]))
                if (alpha,beta) in setA or(beta,alpha) in setA:
                    keepFlag = True
                    count = count + 1
                    if not firstPass:
                        switchFlag = True
                    else:
                        firstPass = False
                elif  keepFlag:
                    keepFlag = False
                    switchFlag = True
        if switchFlag: #tried to put "and len(tempList) is not 0:" here but that didn't work...weird
            if len(tempList) is not 0:
                annList.append(''.join(tempList))
            del tempList[:]
            switchFlag = False
        if keepFlag:
            tempList.append(item)
    else:
        if len(tempList) is not 0:
            annList.append(''.join(tempList))
#    print "gfs annList pre-offal: "+str(len(annList))
# removes extraneous identifier sections from output. Ignored if 'offal' is empty
    if offal: # offal: by-product from the harvest or milling of grain
        kickout = bool
        temp_list = list()
        out_list = list()
        x = list()
        for item in annList:
            kickout = False
            for x in item.split('\n'):
                for off in offal:
                    if re.search(off,x):
                        kickout = True
                if kickout:
                    temp_list.append('\n')
                    break
                else:
                    temp_list.append(x)
                    temp_list.append('\n')
            out_list.append(''.join(temp_list))
            del temp_list[:]
        annList = list(out_list)
    unfound = len(setA) - len(annList)
    return(annList,unfound)
    