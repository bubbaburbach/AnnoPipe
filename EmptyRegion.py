#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import Parsing
import re

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


class fractionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
	if values > 2:
	    parser.error("Max value for threshold is 2".format(option_string))
        setattr(namespace, self.dest,values)
        
        
parser = argparse.ArgumentParser(description= "Comparison program for two genbank style annotation files.")
parser.add_argument("-i","--input", type=str, nargs=2, dest="infiles",required=True)
parser.add_argument("-o","--output", type=str, dest="outfile",required=False)
parser.add_argument("-d","--ident",type=list,nargs="*",default=["  CDS  ","  [trm]RNA  "],dest="ident",required=False, help="Gene identifiers for parsing files. Write for regular expressions. Defaults to '  CDS  ' and '  [trm]RNA  '.")
parser.add_argument("-t","--threshold",action=fractionAction,type=float,dest="threshold",default=0,help=r"Amount of overlap allowed.")
parser.add_argument("-x","--exclude",type=list,nargs="*",dest="exclude",default=[],help='Identifiers to ignore when parsing files. Be exact and explicit, this is very unforgiving. Write for regular expressions, and use quotation marks e.g. " bar ".')
args=parser.parse_args()

fileA = args.infiles[0]
fileB = args.infiles[1]
threshold = args.threshold
ex_ids = list()
ids = list()

if args.outfile is not None:
    outFlag = True
    outFile = args.outfile

for d in args.ident:
    ids.append(re.compile(d))
    
if args.exclude:
    for d in args.exclude:
        e = ''.join(d)
        ex_ids.append(re.compile(e))
        
nameA =fileA.split("/")[-1]
nameB = fileB.split("/")[-1]


altListA,altListB = Parsing.getAltLists(fileA,fileB,ids)

temp = zip(altListA[0],altListA[1])
temp.sort()
altListA = zip(*temp)

temp = zip(altListB[0],altListB[1])
temp.sort()
altListB = zip(*temp)

altListA.append([float(0)]*len(altListA[0]))
altListB.append([float(0)]*len(altListB[0]))


count1 = 0
count2 = 0
    
while count1 < len(altListA[0]):
    while count2 < len(altListB[0]):
        if altListA[0][count1] <= altListB[1][count2] <= altListA[1][count1] or altListA[0][count1] <= altListB[0][count2] <= altListA[1][count1]:
            altListB[2][count2] += float(min(altListB[1][count2],altListA[1][count1])-max(altListB[0][count2],altListA[0][count1]))/float(int(altListB[1][count2])-int(altListB[0][count2]))
            altListA[2][count1] += float(min(altListB[1][count2],altListA[1][count1])-max(altListB[0][count2],altListA[0][count1]))/float(int(altListA[1][count1])-int(altListA[0][count1]))
        if altListB[0][count2] < altListA[0][count1] and altListA[1][count1] < altListB[1][count2]:
            altListB[2][count2] += float(min(altListB[1][count2],altListA[1][count1])-max(altListB[0][count2],altListA[0][count1]))/float(int(altListB[1][count2])-int(altListB[0][count2]))
            altListA[2][count1] += float(min(altListB[1][count2],altListA[1][count1])-max(altListB[0][count2],altListA[0][count1]))/float(int(altListA[1][count1])-int(altListA[0][count1]))
        if altListA[1][count1] < altListB[1][count2]:
            break
        count2+=1
    count2 = 0
    count1 += 1
focusA = set(zip([x[0] for x in zip(altListA[0],altListA[1],altListA[2]) if x[2] < threshold],[x[1] for x in zip(altListA[0],altListA[1],altListA[2]) if x[2] <= threshold]))
focusB = set(zip([x[0] for x in zip(altListB[0],altListB[1],altListB[2]) if x[2] < threshold],[x[1] for x in zip(altListB[0],altListB[1],altListB[2]) if x[2] <= threshold]))
if not outFlag:
    print "From file ",nameA
    print "\t",str(len(focusA))," annotations with less than/equal to ",str(threshold*100),"% overlap"
    print "From file ",nameB
    print "\t",str(len(focusB))," annotations with less than/equal to ",str(threshold*100),"% overlap"
else:
    with open(outFile,'w') as out:
        out.write( "From file "+nameA+"\n")
        out.write( "\t"+str(len(focusA))+" annotations with less than/equal to "+str(threshold*100)+"% overlap\n")
        out.write( "From file "+nameB+"\n")
        out.write( "\t"+str(len(focusB))+" annotations with less than/equal to "+str(threshold*100)+"% overlap\n")
        out.write("\nFrom file "+nameA+"\n")
        out.writelines(Parsing.genesFromSet(fileA,focusA,offal=ex_ids)[0])
        out.write("\n\nFrom file "+nameB+"\n")
        out.writelines(Parsing.genesFromSet(fileB,focusB,offal=ex_ids)[0])