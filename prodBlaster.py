def Main(inList):
    import urllib2
    import string
    from Bio.Blast import NCBIWWW
    from Bio.Blast import NCBIXML
#	import gc
#	import argparse
#	gc.enable()

#	parser = argparse.ArgumentParser(description='BLASTs the protein sequences from prodigal to retrieva protein names')
#	parser.add_argument('-i','--infile',type=str,help="The Annotation Retrieval text file",required=True,dest='infile')
#	parser.add_argument('-o','--out',type=str,help="The output file for the program",default='pb_out.txt',required=True,dest='out')

#	args = parser.parse_args()

#	inList = list()
    pSeq = list()
    pList = list()
    cdsList = list()
    prodList = list()
    outList = list()
    errList = list()
    First = False
    likelyTrans = None 
    maxScore = 0
    min_e = 100
    count = 1
	

#	with open(args.infile,"r") as handle:
#		inList = handle.readlines()

    lastElem = len(inList)-1
    for item in inList:
        if "  CDS  " in item and not First:
            First = True
            cdsList.append(item.strip())
        elif "  CDS  " in item and First:
            pSeq.append(''.join(pList)[:].strip())
            del pList[:]
            cdsList.append(item.strip())
        elif ">" not in item:
            pList.append(item.strip())
        if inList.index(item) == lastElem:
            pSeq.append(''.join(pList)[:].strip())
            del pList[:]
    length = str(len(cdsList))
    for protein in pSeq:
        if "/translation" in protein:
            protein = string.split(protein,"/translation=")[1]
            protein = string.split(protein,"/")[0]
        if protein != '':
            try:
                print "BLASTing "+str(count)+" of "+ length+"."
                blasted = NCBIWWW.qblast("blastp","nr",protein,format_type="XML")
                record = NCBIXML.read(blasted)
    			#likelyTrans = record.alignments[0]
                for records in record.alignments:
                    if records.hsps[0].expect < min_e:
                        maxScore = records.hsps[0].score
                        min_e = records.hsps[0].expect
                        likelyTrans = records
                    elif records.hsps[0].expect == min_e and records.hsps[0].score > maxScore:
                        maxScore = records.hsps[0].score
                        likelyTrans = records
                    prodList.append(str(likelyTrans.title).split(">")[0].split("[")[0].split("|")[-1])
    			#print likelyTrans
                    maxScore = 0
                    min_e = 100

    
            except urllib2.URLError:
                index = pSeq.index(protein)
                errList.append(cdsList.pop(index))
                errList.append(protein)
                pSeq.remove(protein)			
                pass
    
            except urllib2.HTTPError:
                index = pSeq.index(protein)
                errList.append(cdsList.pop(index))
                errList.append(protein)
                pSeq.remove(protein)
                pass
        print "BLASTed "+str(count)
        count += 1
    print pSeq
    i = 0
    while i < len(cdsList):
        outList.append(cdsList[i])
        if len(pSeq[i]) < 45:
            outList.append('\t\t     /translation="'+pSeq[i]+'"')
        else:
            outList.append('\t\t     /translation="'+pSeq[i][:43])
            pSeq[i] = pSeq[i][44:]
            while len(pSeq[i]) > 58:
                outList.append("\t\t     "+pSeq[i][:57])
                pSeq[i] = pSeq[i][58:]
            if pSeq[i] != '':
                outList.append("\t\t     "+pSeq[i]+'"')
            outList.append('\t\t     /product="'+prodList[i]+'"')
        i=i+1

#	gc.disable()
    if len(errList) != 0:
        with open("ErrorDump.txt","w") as errHandle:
            for errItem in errList:
                errHandle.write(errItem + "\n")
            print "Not all proteins were BLASTed due to connection problems.\nCheck 'ErrorDump.txt' for a list of these proteins"
    print "Finished BLASTing"		
    return(outList)
#	with open(args.out,"w") as outFile:
#		for item in outList:
#			outFile.write(item)
