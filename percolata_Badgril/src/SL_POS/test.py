__author__ = 'fengpinghu'
import os,time
import configparser
from public import Autotest
import HTMLTestRunner

def newfile(result_dir):
    '''Find the latest file'''
    # Get all the files in the directory
    lists = os.listdir(result_dir)
    # Re arrange the files in the directory by time.
    lists.sort(key=lambda fn: os.path.getmtime(result_dir+"/"+fn))
    print 'Latest log:'+lists[-1]
    FILE = os.path.join(result_dir,lists[-1])
    return FILE

if __name__ == "__main__":
	now = time.strftime("%Y-%m-%d_%H_%M_%S")
	xmlpath = os.path.split(os.path.realpath(__file__))[0]  # Execution path
	xmlpath2 = xmlpath.split('src')[0]
	LOGFILE = xmlpath2 + 'log/' + now + '_result.html'

	reportname = newfile(xmlpath2 + 'log/')
	print reportname
