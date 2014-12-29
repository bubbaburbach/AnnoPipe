#    import urllib2
import string
import subprocess
from subprocess import PIPE
#    import sys
#    from Bio.Blast import NCBIWWW
#    from Bio.Blast import Applications
from Bio.Blast import NCBIXML
from cStringIO import StringIO
#	import gc
#	import argparse

def Main(inList,cpu_count):

#	gc.enable()

#	parser = argparse.ArgumentParser(description='BLASTs the protein sequences from prodigal to retrieva protein names')
#	parser.add_argument('-i','--infile',type=str,help="The Annotation Retrieval text file",required=True,dest='infile')
#	parser.add_argument('-o','--out',type=str,help="The output file for the program",default='pb_out.txt',required=True,dest='out')

#	args = parser.parse_args()


    # number of cpu's to use while blasting
#    cpu_count = 4
#	inList = list()

    pSeq = list()
    pList = list()
    cdsList = list()
    productList = list()
    outList = list()
#    errList = list()
    translationList = list()
    First = False
    likelyTrans = None 
    maxScore = 0
    min_e = 100
    count = 1
	

#	with open(args.infile,"r") as handle:
#		inList = handle.readlines()

    lastElem = len(inList)-1
    i = 0
    
#    with open("debugIn.txt","w") as debugger:
#        for item in inList:
#            debugger.write(item)
            
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
        if i == lastElem:
            pSeq.append(''.join(pList)[:].strip())
            del pList[:]
        i = i+1
        
    length = str(len(cdsList))
    
#   BLAST each protein sequence
    for protein in pSeq:
        likelyTrans = None
        if "/translation" in protein:
            protein = string.split(protein,"/translation=")[1]
            protein = string.split(protein,"/")[0]
        string.upper(protein)
        if protein != '':
            translationList.append(protein)
            try:
                print("BLASTing "+ str(count)+" of "+length+".")
#                blasted = NCBIWWW.qblast("blastp","nr",protein,format_type="XML")
                cmd = 'blastp -db nr -outfmt 5 -num_threads '+str(cpu_count)+' -query <(echo -e "'+protein+'")'
                blastIt=subprocess.Popen(args=cmd,shell=True,executable="/bin/bash",stdout=PIPE,stderr=PIPE)
                (stdout,stderr)=blastIt.communicate()
                record = NCBIXML.read(StringIO(stdout))
                #likelyTrans = record.alignments[0]
                for records in record.alignments:
                    if records.hsps[0].expect < min_e:
                        maxScore = records.hsps[0].score
                        min_e = records.hsps[0].expect
                        likelyTrans = records
                    elif records.hsps[0].expect == min_e and records.hsps[0].score > maxScore:
                        maxScore = records.hsps[0].score
                        likelyTrans = records
                if likelyTrans is not None:
                    productList.append(str(likelyTrans.title).split(">")[0].split("[")[0].split("|")[-1])
                else:
                    productList.append("No match found in NCBI database.")
                maxScore = 0
                min_e = 100
    
            except OSError:
                print "OS error encountered while attempting 'blastp'. Please verify program paths\nand environment variables, specifically the '$BLASTDB' variable."
                raise(OSError)
#            except urllib2.URLError:
#                index = translationList.index(protein)
#                errList.append(cdsList.pop(index))
#                errList.append(protein)
# #               pSeq.remove(protein)		
#                translationList.remove(protein)
#                pass
#    
#            except urllib2.HTTPError:
#                index = translationList.index(protein)
#                errList.append(cdsList.pop(index))
#                errList.append(protein)
##                pSeq.remove(protein)
#                translationList.remove(protein)
#                pass
        count += 1
    i = 0
#    with open("debug.txt","w") as debug:
#        while i < len(cdsList):
#            debug.write("\t"+cdsList[i])
#            debug.write("\t\t"+pSeq[i])
#            i = i + 1
    while i < len(cdsList):
        outList.append("     "+cdsList[i])
        if len(translationList[i]) < 45:
            outList.append('\t\t     /translation='+translationList[i])
        else:
            outList.append('\t\t     /translation='+translationList[i][:43])
            translationList[i] = translationList[i][44:]
            while len(translationList[i]) > 58:
                outList.append("\t\t     "+translationList[i][:57])
                translationList[i] = translationList[i][58:]
            if translationList[i] != '':
                outList.append("\t\t     "+translationList[i])
        outList.append('\t\t     /product="'+productList[i]+'"')
        i=i+1
#	gc.disable()
#    if len(errList) != 0:
#        with open("ErrorDump.txt","w") as errHandle:
#            for errItem in errList:
#                errHandle.write(errItem + "\n")
#            print "Not all proteins were BLASTed due to connection problems.\nCheck 'ErrorDump.txt' for a list of these proteins"
#    print "Finished BLASTing"		
    return(outList)
#	with open(args.out,"w") as outFile:
#		for item in outList:
#			outFile.write(item)
    
