#! /usr/bin/env python


#import sys
import argparse
import os
import gc
import string
#import subprocess
import re
import Master_Glue
import shutil


############################ FUNCTION DEFINITIONS##########################

# parses fasta and genbank files, breaks the contigs apart, and populates
# a list with the separated contigs/annotations.
# The beginning of a contig or annotation is marked by an identifier
#       usually ">" for fasta and "LOCUS" for genbank
#
# does not work on prodigal files
class fractionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
	if values > 1:
	    parser.error("Max value for threshold is 1".format(option_string))
        setattr(namespace, self.dest,values)

class cpuAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
	if values > 6:
	    parser.error("Max value for cpu_count is 6".format(option_string))
        setattr(namespace, self.dest,values)
	
def parseFile(fileName,identifier):
    flag_first = True
    list_file = list()
    list_a = list()
    list_b = list()
    list_temp = list()
    count_i = 0 
    with open(fileName,'r') as this:
        list_file = this.readlines()
    for item in list_file:
        count_i+=1
        if identifier in item and flag_first:
            del list_temp[:]
            list_temp.append(item)
            matched = re.match(r".*contig\d+",item).group()
            start = string.find(matched,"contig")
            list_a.append(matched[start:])
            flag_first=False
        elif identifier in item:
            list_b.append(''.join(list_temp))
            matched = re.match(r".*contig\d+",item).group()
            start = string.find(matched,"contig")
            list_a.append(matched[start:])
            del list_temp[:]
            list_temp.append(item)       
        elif count_i == len(list_file):
            list_b.append(''.join(list_temp))
            del list_temp[:]
        else:
            list_temp.append(item)
    with open("debug "+fileName.split(".")[-1],"w") as debug:
        debug.write(str(len(list_a))+"\n"+str(len(list_b))+"\n")
        debug.write(list_a[-1]+"\n")
        debug.write(list_b[-1])
    del list_file[:]
    return list_a,list_b

###########################################################################  
########################################################################### 
 
########################INITIALIZATION AND SETUP##########################
if not gc.isenabled():
	gc.enable()

parser = argparse.ArgumentParser("Splits a fasta, genbank, or prodigal file into its individual contigs and populates a folder system with these contigs.\n\n\t Can be used concurrently to group \n\tcontigs with their annotations")
parser.add_argument('-r','--rast',type=str, help="Genbank file with Rast annotation, .gbk file extension.",dest='gbk_Name',required=False)
parser.add_argument('-p','--prod',type=str,help="Text file with Prodigal's annotation. Should have .prod file extension.",dest='prod_Name',required=False)
parser.add_argument('-o','--outfolder',type=str, help="Output folder where the contigs will be stored.",required=True,dest='out')
parser.add_argument('-f','--fasta',type=str, help="Multi Fasta file that contains the contigs associated with the annotations",required=False,dest='fa_Name')
parser.add_argument('-c','--cpu',type=int, help="Dictates number of cpu's to use while BLASTing",default=4,dest='cpu_count',action=cpuAction)
parser.add_argument('-t','--threshold',action=fractionAction, help="Dictates the threshold for difference in gene location comparison.",type=float,dest='threshold')

args=parser.parse_args()
gbk_Name=args.gbk_Name
prod_Name=args.prod_Name
fa_Name=args.fa_Name
outfile=args.out
cpu_count=args.cpu_count
threshold=args.threshold

#if ".fastq" in fa_Name:
#    print "This program does not currently accept fastq files.\nPlease input a fasta file"
#    exit

if not os.path.exists(outfile):
    os.mkdir(outfile)
    
flag_fa = False
flag_gbk = False
flag_prod = False
flag_first = True

list_contigs_a = list()
list_contigs_b = list()
list_file = list()
list_gbkAnnot_a = list()
list_gbkAnnot_b = list()
list_master = list()
list_prodAnnot_a = list()
list_prodAnnot_b = list()
list_temp = list()

dict_master = dict()

###########################################################################


if fa_Name != None:
    flag_fa = True

if gbk_Name != None:
    flag_gbk = True
    
if prod_Name != None:
    flag_prod = True

if not os.path.isdir(outfile):
    os.mkdir(outfile)

if flag_fa:
    print "\nImporting fasta file"
    (list_contigs_a,list_contigs_b) = parseFile(fa_Name,">") 
    for item in list_contigs_a:
        if not dict_master.has_key(item):
            dict_master[item] = item
    print "Dictionary length: "+str(len(dict_master))
    os.chdir(outfile)
    index_for = 1
    for key in dict_master:
        if not os.path.isdir(key):  
            os.mkdir(key)
        os.chdir(key)
        list_local=list()
        i = 0
        for i in range(0,len(list_contigs_a)):
            if list_contigs_a[i] == key:
                list_local.append(list_contigs_b[i])
        with open(key+".fa","w") as fa_out:
            for item in list_local:
                fa_out.write(item)
        del list_local[:]
        index_for = index_for + 1
        os.chdir("..")
    os.chdir("..")
    del list_contigs_b[:]
    del list_contigs_a[:]
    del list_local[:]

if flag_gbk:
    index_for = 1
    print "\nImporting .gbk file"
    (list_gbkAnnot_a,list_gbkAnnot_b) = parseFile(gbk_Name,"LOCUS")
    for item in list_gbkAnnot_a:
        if not dict_master.has_key(item):
            dict_master[item] = item
    print "Dictionary length: "+str(len(dict_master))
    os.chdir(outfile)
    for key in dict_master: 
        if not os.path.isdir(key):  
            os.mkdir(key)
        os.chdir(key)
        i = 0
        list_local = list()
        for i in range(0,len(list_gbkAnnot_b)):
            if list_gbkAnnot_a[i] == key:
                list_local.append(list_gbkAnnot_b[i])
        with open(key+".gbk","w") as gbk_out:
            for item in list_local:
                gbk_out.write(item)
        del list_local[:]   
        os.chdir("..")
    os.chdir("..")
    del list_gbkAnnot_a[:]
    del list_gbkAnnot_b[:]

if flag_prod:
    index_for = 1
    print "\nImporting prod file"
    with open(prod_Name,'r') as prod_File:
        flag_start = False
        for item in prod_File:
            if flag_start:
                list_file.append(item)
            elif "DEFINITION" in item:
                flag_start = True
                list_file.append(item)
    for item in list_file:
        if "DEFINITION" in item:
            matched = re.match(r".*contig\d+",item).group()
            start = string.find(matched,"contig")
            num_contig = matched[start:]
            if dict_master.has_key(num_contig):
                index_contigs = dict_master.get(num_contig)
            else:
                dict_master[num_contig] = num_contig
                index_contigs = dict_master.get(num_contig)
        if "//" in item:
            list_temp.append(item)
            list_prodAnnot_a.append(''.join(list_temp))
            list_prodAnnot_b.append(dict_master.get(index_contigs))
            del list_temp[:]
        else:
            list_temp.append(item)
    del list_file[:]
    print "Dictionary length: "+str(len(dict_master))+"\n"
os.chdir(outfile)
for key in dict_master:  
    if not os.path.isdir(key):  
        os.mkdir(key)
    os.chdir(key)
    i = 0
    list_local = list()
    for i in range(0,len(list_prodAnnot_a)):
        if list_prodAnnot_b[i] == key:
            list_local.append(list_prodAnnot_a[i])
    with open(str(key+".prod"),"w") as prod_out:
        for item in list_local:
            prod_out.write(item)
    index_for = index_for + 1
    os.chdir("..")
os.chdir("..")
gc.disable()

if flag_prod and flag_gbk and flag_fa:
# compare and blast separate contigs and their respective annotations
    os.chdir(outfile)
    for folder in sorted(os.listdir(outfile)):
	print folder
        if folder is not "finalOut.txt":
            os.chdir(outfile+'/'+folder)
            path = outfile+'/'+folder+'/'+folder
            Master_Glue.main(path+'.gbk',path+'.prod',path+'.fa',path+'.out',cpu_count,threshold)
            os.chdir("..")
# concatenate all outputs into single file
    with file("finalOut.txt","w") as final:
        for folder in sorted(os.listdir(outfile)):
            if folder != ("finalOut.txt"):
                focus = file(folder+"/"+folder+".out")
                block = focus.read(65536)
                while block:
                    final.write(block)
                    block = focus.read(65536)
#clean out temp folders and files (not true temp files)
    for folder in sorted(os.listdir(outfile)):
            if folder != ("finalOut.txt"):
                shutil.rmtree(folder)
