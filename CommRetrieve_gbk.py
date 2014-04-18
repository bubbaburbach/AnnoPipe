def Main(infile,gList):
#	import argparse
	import string
	import re

	infileList = list()
	glimmList = list()
	outList = list()

	for item in gList:
		if bool(re.compile('\d').search(item)) and "Unique" not in item:
			glimmList.append(item.translate(None,string.ascii_letters).strip())


	with open(infile,"r") as Infile:
		for item in Infile:
			infileList.append(item)

	for focus in glimmList:
		focusFlag = False
		reverse = ''.join([focus.split('..')[1],'..',focus.split('..')[0]])
		for item in infileList:
			setFlag = False
			if focus in item or reverse in item:
				focusFlag = True
				setFlag = True
			if not setFlag and '..' in item:
				focusFlag = False
			if focusFlag:
				outList.append(item)
#	print outList
	return(outList)			

