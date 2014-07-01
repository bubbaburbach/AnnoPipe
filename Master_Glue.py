#!usr/bin/python


import argparse
import os
import gc
import subprocess
import prodBlaster
import GlimmerComparison
import commonRetrieval
import AnnotationRetrieval_prodigal
import AnnotationRetrieval_genbank
import annotationComparison
import gbkTitleGet
import CommRetrieve_gbk

#### edit this to point to the Glimmer scripts folder
g3Path = "/home/burbs/Programs/Glimmer/glimmer3.02/scripts/"
####

gc.enable()
parser = argparse.ArgumentParser(description="Master file to automatically run the annotation process.")
parser.add_argument('-r','--rast',type=str, help="Genbank file with Rast annotation, .gbk file extension.",dest='gbk_Name')
parser.add_argument('-p','--prod',type=str,help="Text file with Prodigal's annotation. Should have .prod file extension.",dest='prod_Name')
parser.add_argument('-f','--fasta',type=str,help="Fasta file containing the original sequence given to Prodigal and Rast.",dest='fa_Name')
parser.add_argument('-o','--outfile',type=str, help="Final output containing all annotation information",required=False,default="out.txt",dest='out')

args=parser.parse_args()
gbk_Name=args.gbk_Name
prod_Name=args.prod_Name
fa_Name=args.fa_Name
outfile=args.out

comparedLists=annotationComparison.Main(gbk_Name,prod_Name)
differences = comparedLists[0]
common = comparedLists[1]

sequenceList=commonRetrieval.Main(fa_Name,common)

if not os.path.exists(os.path.abspath(".")+"/glimmFolder"):
	subprocess.call("mkdir glimmFolder",shell=True)
	subprocess.call("cd glimmFolder",shell = True)
	cleaned = fa_Name.replace(' ','\ ')
	print "\n\n"
    	subprocess.call(g3Path+"g3-iterated.csh "+fa_Name+" "+"glimmFolder/"+cleaned.split(".")[-2].split("/")[-1]+"_temp",shell=True)
	subprocess.call("cd ..",shell=True)
else:
	print "\n\nglimmFile folder already exists\n\nskipping glimmer"


placeHolderList3=GlimmerComparison.Main(differences,os.getcwd()+"/glimmFolder/"+fa_Name.split(".")[-2].split("/")[-1]+"_temp.predict")
placeHolderList1=AnnotationRetrieval_genbank.Main(gbk_Name,placeHolderList3)
placeHolderList2=AnnotationRetrieval_prodigal.Main(prod_Name,placeHolderList3)
placeHolderList5=CommRetrieve_gbk.Main(gbk_Name,common)
titleList = gbkTitleGet.Main(gbk_Name)

for item in placeHolderList2:
	placeHolderList1.append(item)

placeHolderList4=prodBlaster.Main(placeHolderList1)
outList = titleList + placeHolderList5 + placeHolderList4

gc.disable()

with open(outfile,"w") as output:
    for item in outList:
        output.write(item.rstrip()+"\n")
    output.write("//")
