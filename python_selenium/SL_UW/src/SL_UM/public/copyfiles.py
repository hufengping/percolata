# -*- coding: utf-8 -*- 
'''
Created on 2015年3月24日

@author: fengping.hu
'''
import os 
import time,datetime,string
from os import listdir
from os.path import isdir
from stat import *

inipath1 = os.path.split(os.path.realpath(__file__))[0] #获取当前路径
inipath2 = inipath1.split('src')[0]

source = inipath2+r"log" 
target_dir = inipath2+r"new"
if isdir(source) != True:
    print 'Error: source is not a directory'
    exit()
filelist = listdir(source)
for name in filelist :
    strr = source+"\\"+name
    trrr = target_dir+"\\"+name
    t1 = time.gmtime(os.stat(strr)[ST_MTIME]) #get file's mofidy time
    t11 = time.strftime('%Y-%m-%d',t1)
    year,month,day=t11.split('-')
    t111= datetime.datetime(int(year),int(month),int(day))
    t2 = time.gmtime()
    t22 = time.strftime('%Y-%m-%d',t2)
    year,month,day=t22.split('-')
    t222= datetime.datetime(int(year),int(month),int(day))
    days = (t222-t111).days
    if days < string.atof('1') :
        os.system("copy %s %s" % (strr, trrr.strip()))
