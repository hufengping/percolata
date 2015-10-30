#!/usr/bin/env python
# coding=utf-8

import unittest
import HTMLTestRunner
import time, os, sys
import configparser
from public import Autotest


# Defining search method of testcase,return testsuite
def creatsuite():
	testunit = unittest.TestSuite()
	# Test file search directory
	test_dir = xmlpath
	# dfine parameter of discover
	discover = unittest.defaultTestLoader.discover(test_dir,
												   pattern='test*.py',
												   top_level_dir=None)
    # add testcases to test suite
	for test_suite in discover:
		for test_cases in test_suite:
			testunit.addTest(test_cases)
			print testunit
	return testunit


# Get the time now
now = time.strftime("%Y-%m-%d_%H_%M_%S")
# Define director for test report
xmlpath = os.path.split(os.path.realpath(__file__))[0]  # Execution path
xmlpath2 = xmlpath.split('src')[0]
LOGFILE = xmlpath2 + 'log/' + now + '_result.html'

# read credentials
CREDENTIALS_FILE = 'public/.credentials'
config = configparser.ConfigParser()
config.read(CREDENTIALS_FILE)
mail_from = config['MAIL']['FROM']
mail_to = config['MAIL']['TO']

fp = file(LOGFILE, 'wb')
runner = HTMLTestRunner.HTMLTestRunner(
	stream=fp,
	title=u'Percolata Test Repot',
	description=u'Test case execution:')
if __name__ == '__main__':
	# Check test data for updates
	#db2file.updataFile()

	alltestnames = creatsuite()
	runner.run(alltestnames)
	fp.close()
	reportname = Autotest.newfile(xmlpath2 + 'log/')
	f = open(reportname)
	txt = f.read()
	Autotest.mail(mail_to, 'Auto test results', txt, reportname)
# copy files to jenkins log
