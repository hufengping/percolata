#/usr/bin/env python
#coding=utf-8

import os
import filesCount as fc
"""
List all the files in current directory which is end of ".txt"
Count the number in each file like "count: 23" in second times.
"""

count=0
filelist = fc.GetFileList(os.getcwd(),".txt")
for files in filelist:
	print files
	with open(files) as f:
		str1 = f.read()
		a = str1.split("count:",3)[2]
		b = a.split("time")[0]
		count = count + int(b)
	print "This file:%r Count: %r" %(b, count)
