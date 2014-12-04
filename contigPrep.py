# -*- coding: utf-8 -*-
#! /usr/bin/env python

import argparse
import os

def extCheck(choices):
    class Act(argparse.Action):
        def __call__(self,parser,namespace,fname,option_string=None):
            ext = os.path.splitext(fname)[1][1:]
            if ext not in accepted:
                parser.error("Input does not have proper extension. Accepts {} files.".format(accepted))
        return fname
    
accepted = set('fna','fa','fasta','fas')
parser=argparse.ArgumentParser(usage="./contigPrep.py -i [fasta file]", description="Preps fasta files for use in the pipeline. Replaces contig identifiers with a number indicating their order in the file. Should be run first, before using any annotation services.")
parser.add_argument('-i','--input',dest='infile',required=True,action=extCheck(),help="Input file. Takes fasta files.")
parser.add_argument('-t','--track',dest='track',type = bool,required = False,default = True, help = "Track is enabled by default. Creates a second file listing original and altered contig identifiers.")
args=parser.parse_args()
    
fname = args.infile
track = args.track
count = int()
padding = int()
list_file = list()
list_out = list()
list_orig = list()

with open(fname,"w+") as fileFocus:
    count = 0
    for item in fileFocus:
        if '>' in item:
            count = count + 1
        list_file.append(item)
        
    padding = len(str(count))
    count = 0
    for item in list_file:
        if '>' in item:
            count = count + 1
            padded = '>'+'0'*(padding-len(str(count))+str(count))
            list_out.append(padded)
            if track:
                list_orig.append((item,padded))
        else:
            list_out.append(item)
    fileFocus.writelines(list_out)

if track:
    with open(os.path.split(fname)+'giInfo.txt','w') as giFile:
        giFile.writelines(list_orig)