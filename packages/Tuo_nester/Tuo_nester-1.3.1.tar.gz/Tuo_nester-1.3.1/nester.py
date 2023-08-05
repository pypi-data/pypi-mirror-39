# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 00:19:24 2018

@author: neptune.sun
"""
import sys
#indent控制是否缩进，默认否；level控制缩进级数，默认0;fh控制输出位置，默认标准输出
def print_lol(the_list,indent=False,level=0,fh=sys.stdout): 
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='',file=fh)
            print(each_item,file=fh)