def Main(infile,glimm):
#	import argparse
    import string
    import re

#	parser = argparse.ArgumentParser(description='Compare output of annotationComparison.py with the output of Glimmer')
#	parser.add_argument('-i','--infile',type=str,help="The original prodigal (.prod) annotation file",required=True,dest='infile')
#	parser.add_argument('-g','--glimm',type=str,help="The GlimmerComparison.py output file",required=True,dest='glimm')
#	parser.add_argument('-o','--out',type=str,help="The output file for the program",default='out.txt',required=True,dest='out')

#	args = parser.parse_args()

    infileList = list()
    glimmList = list()
    cdsList = list()
    outList = list()

    keepFlag = False
#	print glimm
#	with open(glimm,"r") as glimFile:
    for item in glimm:
        shiftFlag = False
        if "Unique" in item and ".prod" in item:
            keepFlag = True
            shiftFlag = True
        elif keepFlag:
            if bool(re.compile('\d').search(item)):
                glimmList.append(item.translate(None,string.ascii_letters).translate(None,"()").strip())
            if not shiftFlag:
                keepFlag = False
    with open(infile,"r") as inFile:
        for item in inFile:
            if "  CDS  " in item:
                cdsList.append(item)
            else:
                infileList.append(item)
    for focus in glimmList:
        focusFlag = False
        reverse = ''.join([focus.split('..')[1],'..',focus.split('..')[0]])
        geneCount = 0
        geneGrab = None
        flag_grab = False
        for item in cdsList:
            geneCount = geneCount + 1
            if focus in item or reverse in item:
                outList.append(item)
                geneGrab = geneCount
                flag_grab = True
            if flag_grab:
                for item in infileList:
                    setFlag = False
                    if "Gene "+str(geneGrab)+" " in item:
                        focusFlag = True
                        setFlag = True
                    if not setFlag and '>' in item:
                        focusFlag = False
                    if focusFlag:
                        outList.append(item)
                break
                        
    return(outList)
#	with open(args.out,'w') as outFile:
#		for item in outList:
#			outFile.write(item)
