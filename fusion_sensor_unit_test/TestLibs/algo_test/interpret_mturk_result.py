#!/usr/bin/env python

import os
import sys
from optparse import OptionParser
import json

def parse_option_args():
    parser = OptionParser()
    parser.add_option("-f","--filename",help="the target result file would be interpreted.")

    (options, args) = parser.parse_args()

    filename = options.filename
    if not filename==None:
        return filename
    else:
	print('''Usage: interpret_mturk_result.py [options]
Options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename=FILENAME
                        the target result file would be interpreted.''')
	sys.exit(1)

def parse_mturk_result(resultFile):
    with open(resultFile) as f:
        to_left=0
        to_right=0
        _result = json.load(f)
        if not "labeling" in _result:
            return (to_left, to_right)

        else:
            for item in _result["labeling"]:
                if item[1] == 1:
                    to_left += 1
                if item[2] == 1:
                    to_right += 1

            return (to_left, to_right)


if __name__ == '__main__':
    _resultFile = parse_option_args()

    print(parse_mturk_result(_resultFile))


