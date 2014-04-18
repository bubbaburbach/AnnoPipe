def Main(fileA,listB):
#	import sys
    import string


    contigList = list()
    commonList = list()
    sequenceList = list()
    transTable = string.maketrans("ATCG","TAGC")
    
    
    
    with open(fileA,'r') as contigFile:
        for item in contigFile:
	    if '>' not in item:
             contigList.append(item.strip())
	
#	commonFlag=False
#	with open(fileB,'r') as compFile:
#	for item in fileB:
    for item in listB:
	    revFlag = False
#		if commonFlag == True:
	    if "complement" in item:
             revFlag = True
	    commonList.append([item.translate(None,string.ascii_letters).translate(None,"()").strip(),revFlag])
#		if "Common" in item:
#			commonFlag = True
	
    contig = ''.join(contigList)
    seqCount = 1
    for item in commonList:
	    focus = item[0].split("..")
	    sequenceList.append(''.join(['>SEQ',str(seqCount),'  ',focus[0],' ',focus[1],'  len=',str(int(focus[1])-int(focus[0]))]))
	    if item[1]:
		    section = contig[int(focus[0])-1:int(focus[1])-1].translate(transTable)
		    sequenceList.append(section)
	    else:
		    sequenceList.append(contig[int(focus[0])-1:int(focus[1])-1])
	    seqCount = seqCount + 1
    with open("trainingSet.fa.temp",'w') as output:
	    output.write('\n'.join(sequenceList))
    return(sequenceList)
