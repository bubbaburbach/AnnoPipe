import string
import re
def Main(infile,glimm):
#	import argparse


	#add option for multiple .gbk files low priority

#	parser = argparse.ArgumentParser(description='Compare output of annotationComparison.py with the output of Glimmer')
#	parser.add_argument('-i','--infile',type=str,help="The original genbank (.gbk) annotation file",required=True,dest='infile')
#	parser.add_argument('-g','--glimm',type=str,help="The GlimmerComparison.py output file",required=True,dest='glimm')
#	parser.add_argument('-o','--out',type=str,help="The output file for the program",default='out.txt',required=True,dest='out')

#	args = parser.parse_args()

    infileList = list()
    glimmList = list()
    outList = list()

    keepFlag = False
#	with open(args.glimm,"r") as glimFile:
    for item in glimm:
        if "Unique" in item and ".gbk" in item:
            keepFlag = True
        if "BASE " in item:
            keepFlag = False
        if keepFlag:
            if "Unique" in item and ".prod" in item:
                keepFlag = False
            if bool(re.compile('\d').search(item)) and "Unique" not in item:
                glimmList.append(item.translate(None,string.ascii_letters).translate(None,"()").strip())


    with open(infile,"r") as Infile:
        for item in Infile:
            infileList.append(item)

    for focus in glimmList:
        focusFlag = False
        reverse = ''.join([focus.split('..')[1],'..',focus.split('..')[0]])
        for item in infileList:
            setFlag = False
            if "BASE COUNT" in item:
                focusFlag = False
            elif focus in item or reverse in item:
                focusFlag = True
                setFlag = True
            elif not setFlag and '..' in item:
                focusFlag = False
            if focusFlag:
                outList.append(item)

#	print outList
    return(outList)			
#	with open(args.out,'w') as outFile:
#		for item in outList:
#			outFile.write(item)
