def Main(gbkFile):
	
	titleList = list()
	titleEnd = False
	with open(gbkFile,"r") as gbkFile:
		for item in gbkFile:
			if titleEnd == True:
				break
			else:
				if "     CDS      " in item:
					titleEnd = True
				else:
					titleList.append(item)

	return(titleList)
