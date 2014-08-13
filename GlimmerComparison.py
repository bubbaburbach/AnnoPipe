def Main(inList,glimm):
#	import argparse
    import string
    import re
    import os

#	parser = argparse.ArgumentParser(description='Compare output of annotationComparison.py with the output of Glimmer')
#	parser.add_argument('-i','--infile',type=str,help="The difference file from annotationComparison.py",required=True,dest='infile')
#	parser.add_argument('-g','--glimm',type=str,help="The .predict file from Glimmer",required=True,dest='glimm')
#	parser.add_argument('-o','--out',type=str,help="The output file for the program",default='out.txt',required=True,dest='out')

#	args = parser.parse_args()
    glimSet = set()
    origList = list()
    geneList = list()
    commonList = list()
    commonFlag = False
    non_decimal = re.compile(r'[^\d.]+')

#	with open(args.infile,"r") as origFile:
    for item in inList:
        if "Common" in item:
            commonFlag = True
        if commonFlag:
            commonList.append(item)
        elif item != "\n":
            origList.append(item)

    if not os.path.isfile(glimm):
        temp = glimm.split(".")
        glimm = ".run1.".join(temp)
    
    if os.path.isfile(glimm):
        with open(glimm,"r") as glimFile:
            for item in glimFile:
                if "orf" in item:
                    focus = item.split()
                    focus[1] = non_decimal.sub('',focus[1])
                    focus[2] = non_decimal.sub('',focus[2])
                    if int(focus[1]) > int(focus[2]):
                        a = focus[1][:]
                        focus[1] = focus[2][:]
                        focus[2] = a[:]
                    glimSet.add((int(focus[1]),int(focus[2])))
        count = 0
        for item in origList:
            count = count+1
            if 'Unique' in item:
                geneList.append(item)
            elif item != ' ':
                focus = re.split('[().]',item.translate(None,string.ascii_letters).translate(None,"()").strip())
                focus[0] = non_decimal.sub('',focus[0])
                focus[2] = non_decimal.sub('',focus[2])
                if int(focus[0]) < int(focus[2]):
                    if (int(focus[0]),int(focus[2])) in glimSet:
                        geneList.append(item)
                elif (int(focus[2]),int(focus[0])) in glimSet:
                    geneList.append(item)
    else:
        print "Glimm file not found"
                    
    for item in commonList:
        geneList.append(item)
        
    return(geneList)
#	with open(args.out,"w") as handle:
#		for item in geneList:
#			handle.write(item)
#		handle.write("\n")
#		for item in commonList:
#			handle.write(item)
