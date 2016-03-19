#!/usr/bin/env python
# created by Yifei.Fu at 2015-01-21

import os
import sys
import pexpect
import time
import tempfile
import json
import glob
config_file = './config_test.json'


def parse_config(filename):
    configurations = {}

    try:
        with open(filename, 'r') as config:
            # parse config_file
            configurations = json.load(config)
    except IOError as err:
        print('open config file failure.\n')
        raise Exception("cannot open config file.")

    return configurations
# end of parse_config


if __name__ == '__main__':
    """check if the dp server has specified files in specified dir
    sys.argv[1]: dirName to be check
    sys.argv[2]: Pattern of target file
    sys.argv[3]: optional, default 1, expected number of matched files"""
    conf = parse_config(config_file)
    from interact import *

    dirName = sys.argv[1]
    filePattern = sys.argv[2]
    expNum = 1
    if (len(sys.argv) > 3):
        expNum = int(sys.argv[3])

    os.chdir(dirName)
    matchedList = glob.glob('*%s*' % (filePattern))

    if(expNum > matchedList.__len__()):
        print('check file existence failure.\n')
        sys.exit(1)
    elif(expNum <= matchedList.__len__()):
        pass
    else:
        print('abortion failure.\n')

    # report
    print('check file successful.\n')
