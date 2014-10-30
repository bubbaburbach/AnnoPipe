#! /usr/bin/env python
import os
import gc
import subprocess
import prodBlaster
import GlimmerComparison
#import commonRetrieval
import AnnotationRetrieval_prodigal
import AnnotationRetrieval_genbank
import annotationComparison
import gbkTitleGet
import CommRetrieve_gbk

def main(gbk_in,prod_in,fa_in,out_in,cpu_count,diffAllow):
    #import argparse

    
    #### edit this to point to the Glimmer 'scripts' folder####
    g3Path = "/home/adam/Programs/Glimmer/glimmer3.02/scripts/"
    #########################################################
    
    gc.enable()
    #parser = argparse.ArgumentParser(description="Master file to automatically run the annotation process.")
    #parser.add_argument('-r','--rast',type=str, help="Genbank file with Rast annotation, .gbk file extension.",dest='gbk_Name')
    #parser.add_argument('-p','--prod',type=str,help="Text file with Prodigal's annotation. Should have .prod file extension.",dest='prod_Name')
    #parser.add_argument('-f','--fasta',type=str,help="Fasta file containing the original sequence given to Prodigal and Rast.",dest='fa_Name')
    #parser.add_argument('-o','--outfile',type=str, help="Final output containing all annotation information",required=False,default="out.txt",dest='out')
    
    #args=parser.parse_args()
    gbk_Name=gbk_in
    prod_Name=prod_in
    fa_Name=fa_in
    outfile=out_in
    placeHolderList4 = list()
    ### Compare the .gbk and .prod annotations
    ### keeping what they agree on in 'common'
    ### differences are kept in 'differences'

    (differences,common)=annotationComparison.Main(gbk_Name,prod_Name,diffAllow)
    
    ### Retrieves the nucleotide sequences associated
    ### with the common proteins.
    ### Used to create training sequences for Glimmer
    
    print str(len(differences[0])+len(differences[1]))+" mismatches"
    if not os.path.exists(os.path.abspath(".")+"/glimmFolder"):
        subprocess.call("mkdir glimmFolder",shell=True,executable="/bin/bash")
        subprocess.call("cd glimmFolder",shell = True)
        cleaned = fa_Name.replace(' ','\ ')
        call = g3Path+'g3-iterated.csh '+cleaned+' ' +"glimmFolder/"+cleaned.split(".")[-2].split("/")[-1]+'_temp'
        subprocess.call(call,shell=True,executable="/bin/csh")
        subprocess.call("cd ..",shell=True)
    else:
    	print "\n\nglimmFile folder already exists\n\nskipping glimmer"
    #RNA_List=RNA_retrieve.Main(gbk_Name)
    ## Compares the difference list against the Glimmer ORF'
    placeHolderList3=GlimmerComparison.Main(differences,os.getcwd()+"/glimmFolder/"+fa_Name.split(".")[-2].split("/")[-1]+"_temp.predict",diffAllow)   
    placeHolderList1=AnnotationRetrieval_genbank.Main(gbk_Name,placeHolderList3[0])
    placeHolderList2=AnnotationRetrieval_prodigal.Main(prod_Name,placeHolderList3[1])
    
    # Retrieve the verified genes' information from the genbank file 
    common = common + placeHolderList1
    placeHolderList5=CommRetrieve_gbk.Main(gbk_Name,common)
    titleList = gbkTitleGet.Main(gbk_Name)
    
    #placeHolderList1 = placeHolderList1 + placeHolderList2
    
    # Run remaining protein sequences through the NCBI database using BLAST
    try:
        placeHolderList4=prodBlaster.Main(placeHolderList2,cpu_count)
    except OSError:
        raise
    
    # Next step is sort the genes based on location
    
    outList = titleList + placeHolderList5 + placeHolderList4
    
    gc.disable()
    
    with open(outfile,"w") as output:
        for item in outList:
            output.write(item.rstrip()+"\n")
        output.write("//\n")
