# -*- coding: utf-8 -*-
def equivIndices(altList1,altList2,diffAllow):
    count1 = 0
    count2 = 0
    outList= list()
    locList1 = list(altList1)
    locList2 = list(altList2)
    while count1 < len(locList1[0]):
        loc1 = [locList1[0][count1],locList1[1][count1]]
        if locList1[0][count1] > locList1[1][count1]:
            loc1 = [locList1[1][count1],locList1[0][count1]]    
        while count2 < len(locList2[0]):
            loc2 = [locList2[0][count2],locList2[1][count2]]
            if locList2[0][count2] > locList2[1][count2]:
                loc2 = [locList2[1][count2],locList2[0][count2]]
            if loc2[1] == -1:
                count2 = count2 + 1
            elif (((abs(float(loc1[0])-float(loc2[0]))) + (abs(float(loc1[1])-float(loc2[1]))))/(((float(loc2[1])-float(loc2[0]))+(float(loc1[1])-float(loc1[0])))/2)) <= diffAllow:
                outList.append(count1)
                locList1[0][count1] = -1
                locList1[1][count1] = -1
                locList2[0][count2] = -1
                locList2[1][count2] = -1
                break
            else:
                count2 = count2+1
        count1 += 1
        count2 = 0
    return outList
        
def equivIndicesBoth(altList1,altList2,diffAllow):
    count1 = 0
    count2 = 0
    outList= [[],[]]
    locList1 = list(altList1)
    locList2 = list(altList2)
    while count1 < len(locList1[0]):
        loc1 = [locList1[0][count1],locList1[1][count1]]
        if locList1[0][count1] > locList1[1][count1]:
            loc1 = [locList1[1][count1],locList1[0][count1]]    
        while count2 < len(locList2[0]):
            loc2 = [locList2[0][count2],locList2[1][count2]]
            if locList2[0][count2] > locList2[1][count2]:
                loc2 = [locList2[1][count2],locList2[0][count2]]
            if loc2[1] == -1:
                count2 = count2 + 1
            elif (((abs(float(loc1[0])-float(loc2[0]))) + (abs(float(loc1[1])-float(loc2[1]))))/(((float(loc2[1])-float(loc2[0]))+(float(loc1[1])-float(loc1[0])))/2)) <= diffAllow:
                outList[0].append(count1)
                outList[1].append(count2)
                locList1[0][count1] = -1
                locList1[1][count1] = -1
                locList2[0][count2] = -1
                locList2[1][count2] = -1
                break
            else:
                count2 = count2+1
        count1 += 1
        count2 = 0
    return outList
