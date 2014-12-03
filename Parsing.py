# -*- coding: utf-8 -*-
import re

cds_template = re.compile("  CDS  ")
rna_template = re.compile("  [trm]RNA  ")
gene_template = re.compile("   gene  ")
non_decimal = re.compile(r'[^\d.]+')

id_default = [cds_template,rna_template]#,gene_template]

def findPoles(listA,listB):
    altList1 = [[],[]]
    altList2 = [[],[]]
    for item in listA:
        num = item.strip().replace(",","..").split("..")[-2]
        pole = non_decimal.sub('',num)
        altList1[0].append(pole[:])
        num = item.strip().replace(",","..").split("..")[-1]
        pole = non_decimal.sub('',num)
        altList1[1].append(pole[:])
            
    for item in listB:
        num = (item.strip().replace(",","..").split("..")[-2])
        pole1 = non_decimal.sub('',num)
        altList2[0].append(pole1[:])
        num = (item.strip().replace(",","..").split("..")[-1])
        pole1 = non_decimal.sub('',num)
        altList2[1].append(pole1[:])
    return altList1,altList2
    
def sortPoles(altList1,altList2):
    #sorting poles so it always reads (low,high)
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
# creates altLists used in location comparisons
    inListA = grabLocs(fileA,identifiers)
    inListB = grabLocs(fileB,identifiers)
    altList1,altList2 =findPoles(inListA,inListB)        
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
            if 'BASE COUNT' in line:
                break
            else:
                inList.append(line) 

    for item in inList:
        for xx in identifiers:
            if re.search(xx,item):
                alpha = non_decimal.sub('',item.split()[1].split('..')[0])
                beta = non_decimal.sub('',item.split()[1].split('..')[1])
                if (alpha,beta) in setA or(beta,alpha) in setA:
                    keepFlag = True
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
# removes extraneous identifier sections from output. Ignored if 'offal' is not empty
    if offal: # offal: by-product from the harvest or milling of grain
        kickout = False
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
                    break
                else:
                    temp_list.append(x)
           # else:
            #    temp_list.append('\n')
            out_list.append('\n'.join(temp_list))
        annList = list(out_list)
            
                
    unfound = len(setA) - len(annList)
    return(annList,unfound)
    