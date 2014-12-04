#! /usr/bin/env python
#"""
#Created on Wed Nov  5 18:51:57 2014
#
#@author: adam
#"""

import argparse
import re
import Parsing
import _geneEquivalence
class fractionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
	if values >= 1:
	    parser.error("Max value for threshold is 1".format(option_string))
        setattr(namespace, self.dest,values)
        
outFlag = False
outFile = None

inListA = list()
inListB = list()
uniqListA = list()
uniqListB = list()
altListA = [[],[]]
altListB = [[],[]]
outListA = list()
outListB = list()

loc_dict = dict()

nameA = str()
nameB = str()

cds_template = re.compile("  CDS  ")
rna_template = re.compile("  [trm]RNA  ")
non_decimal = re.compile(r'[^\d.]+')




parser = argparse.ArgumentParser(description= "Comparison program for two genbank style annotation files.")
parser.add_argument("-i","--input", type=str, nargs=2, dest="infiles",required=True)
parser.add_argument("-o","--output", type=str, dest="outfile",required=False)
parser.add_argument("-d","--ident",type=list,nargs="*",default=["  CDS  ","  [trm]RNA  "],dest="ident",required=False, help="Gene identifiers for parsing files. Write for regular expressions. Defaults to '  CDS  ' and '  [trm]RNA  '.")
parser.add_argument("-t","--threshold",action=fractionAction,type=float,dest="threshold",default=0,help=r"Difference threshold for comparing gene locations. Takes floats between 0 and 1. (exact - 100%% gene length offset)")
parser.add_argument("-x","--exclude",type=list,nargs="*",dest="exclude",default=[],help="Identifiers to ignore when parsing files. Be exact and explicit, this is very unforgiving. Write for regular expressions.")
args=parser.parse_args()

fileA = args.infiles[0]
fileB = args.infiles[1]
threshold = args.threshold
ex_id = list()
ids = list()

if args.outfile is not None:
    outFlag = True
    outFile = args.outfile

for d in args.ident:
    ids.append(re.compile(d))

if args.exclude:
    for d in args.exclude:
        e = ''.join(d)
        ex_id.append(re.compile(e))
        
nameA =fileA.split("/")[-1]        
nameB = fileB.split("/")[-1]

altListA,altListB = Parsing.getAltLists(fileA,fileB,identifiers=ids)



if threshold == 0:    
    loc_setA = set(zip(altListA[0],altListA[1]))
    loc_setB = set(zip(altListB[0],altListB[1]))
    common_set = loc_setA & loc_setB
    uniqA_set = loc_setA - loc_setB
    uniqB_set = loc_setB - loc_setA    
else:
    print len(altListA[0])," ",len(altListA[1])," ",len(altListB[0])," ",len(altListB[1])
    common_set=set(_geneEquivalence.locEquivalent(altListA,altListB,threshold))
    uniqA_set = set(zip([x for x in altListA[0] if x != -1],[y for y in altListA[1] if y != -1]))
    uniqB_set = set(zip([x for x in altListB[0] if x != -1],[y for y in altListB[1] if y != -1]))    
    
if not outFlag:
    print len(altListA[0])," from ",nameA
    print len(altListB[0])," from ",nameB
    print len(common_set)," common to both"
    print len(uniqA_set)," unique in ",nameA
    print len(uniqB_set)," unique in ",nameB
else:
    uniqListA,errA = Parsing.genesFromSet(fileA,uniqA_set,identifiers=ids,offal=ex_id)
    uniqListB,errB = Parsing.genesFromSet(fileB,uniqB_set,identifiers=ids,offal=ex_id)
    #insert error statement here maybe?
            
        
    with open(outFile,'w') as out:
        out.write(str(len(altListA[0]))+" from "+nameA+"\n")
        out.write( str(len(altListB[0]))+" from "+nameB+"\n")
        out.write( str(len(common_set))+" common to both\n")
        out.write( str(len(uniqA_set))+" unique in "+nameA+"\n")
        out.write( str(len(uniqB_set))+" unique in "+nameB+"\n")
        out.write( "\n\nUnique annotations in "+nameA+"\n")
        for item in uniqListA:
            out.write(item)
        out.write( "\n\nUnique annotations in "+nameB+"\n")
        for item in uniqListB:
            out.write( item)
