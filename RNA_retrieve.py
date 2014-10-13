# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 17:49:50 2014

@author: adam
"""
import re

def Main(fileName):
    
    list_RNA = list()
    list_Loc = list()
    list_temp = list()
    
    flag_keep = False
    flag_switch = False
    
    template_rna = re.compile('  [tmr]RNA  ')
    template_cds = re.compile(' CDS ')
    template_bc = re.compile('BASE COUNT')
    
    with open(fileName) as fN:
        for item in fN:
            if re.search(template_rna,item):
                flag_keep = True
                flag_switch = True
            if re.search(template_cds,item) or re.search(template_bc,item):
                flag_keep = False
                flag_switch = True
            if flag_switch and len(list_temp) is not 0:
                list_RNA.append(''.join(list_temp))
                del list_temp[:]
                flag_switch = False
            if flag_keep:
                list_temp.append(item)
        else:
            if len(list_temp) is not 0:
                list_RNA.append(''.join(list_temp))
                del list_temp[:]
    for item in list_RNA:
        focus = item.split()[1].split('..')
        list_Loc.append(focus[:])
    return list_RNA, list_Loc