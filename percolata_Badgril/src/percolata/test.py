__author__ = 'fengpinghu'
# coding=utf-8
import os
from public import Autotest
xmlpath = os.path.split(os.path.realpath(__file__))[0]  # Execution path
xmlpath2 = xmlpath.split('src')[0]
reportname = Autotest.newfile(xmlpath2 + 'log/')

f = open(reportname)
txt = f.read()
Autotest.mail("fengping.hu@percolata.com", "Test Report", txt)