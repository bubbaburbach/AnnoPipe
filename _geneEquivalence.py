# -*- coding: utf-8 -*-

#import argparse


#def required_length(nmin,nmax):
#    class RequiredLength(argparse.Action):
#        def __call__(self, parser, args, values, option_string=None):
#            if not nmin<=len(values)<=nmax:
#                msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
#                    f=self.dest,nmin=nmin,nmax=nmax)
#                raise argparse.ArgumentTypeError(msg)
#            setattr(args, self.dest, values)
#    return RequiredLength
    

def locEquivalent(altList1,altList2,diffAllow=.01):
    count1 = 0
    count2 = 0
    tempList = list()
    print len(altList2[1])#
    print len(altList2[0])#
    while count1 < len(altList1[0]):
        loc1 = [altList1[0][count1],altList1[1][count1]]
        if altList1[0][count1] > altList1[1][count1]:
            loc1 = [altList1[1][count1],altList1[0][count1]]    
        while count2 < len(altList2[0]):
            #if count2 == 0:
                #print "IN WHILE"
            loc2 = [altList2[0][count2],altList2[1][count2]]
            if altList2[0][count2] > altList2[1][count2]:
                loc2 = [altList2[1][count2],altList2[0][count2]]
            if loc2[1] == -1:
                count2 = count2 + 1
            elif (((abs(float(loc1[0])-float(loc2[0]))) + (abs(float(loc1[1])-float(loc2[1]))))/(((float(loc2[1])-float(loc2[0]))+(float(loc1[1])-float(loc1[0])))/2)) < diffAllow:
                tempList.append(str(altList1[0][count1][:])+'..'+str(altList1[1][count1][:]))
                altList1[0][count1] = -1
                altList1[1][count1] = -1
                altList2[0][count2] = -1
                altList2[1][count2] = -1
                break
            else:
                count2 = count2+1
        count1 += 1
        count2 = 0
    #print tempList
    return(tempList)


   
#parser = argparse.ArgumentParser(description='Compare gene locations .')
#parser.add_argument('-g','--gbk',nargs = '*',action = required_length(1,2),dest='gbk')
#parser.add_argument('-p','--prod',nargs = '*',action = required_length(1,2),dest='prod')
#parser.add_argument('-r','--rna',nargs = '*',action = required_length(1,2),dest='rna')
#parser.add_argument('-o','--out',default = 'out.txt',dest='out')
#
#args = parser.parse_args()
#
#gbk = args.gbk
#prod = args.prod
#rna = args.rna
#out = args.out
#
#fCount = 0
#maxFiles = 2
