#!/usr/bin/env python

import os
import sys
from optparse import OptionParser
import json
import pexpect

def parse_option_args():
    parser = OptionParser()
    parser.add_option("-f","--filename",help="the target result file would be interpreted.")
    parser.add_option("-o","--output",help="download file's save pathName.")

    (options, args) = parser.parse_args()

    filename = options.filename
    output = options.output
    if not (filename==None or output==None):
        return (filename,output)
    else:
	print('''Usage: interpret_mturk_result.py [options]
Options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename=FILENAME
                        the target result file would be interpreted
  -o OUTPUT, --output=OUTPUT
			the download file's save pathName.''')
	sys.exit(1)

def downloader(resultFileName, saveFileName):
    with open(resultFileName,'r') as fp:
	filePath = json.load(fp)["header"]["filepath"]
	pexpect.run("scp zm:%s %s"%(filePath, os.path.abspath(saveFileName)))
	#print("scp zm:%s %s"%(filePath, os.path.abspath(saveFileName)))

if __name__ == '__main__':
    (_resultFile, saveFileName) = parse_option_args()
    downloader(_resultFile, saveFileName) 


