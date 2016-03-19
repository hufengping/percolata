#!/usr/bin/env python
# created by Yifei.Fu at 2015-04-01

import os
import sys
import pexpect
import time
import inspect
import json
import glob
import re
from interact import *
config_file = './config_test.json'


def get_script_dir():
    self = inspect.stack()[0][1]
    return os.path.abspath(os.path.dirname(self))
# end of get_script_dir


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
    sys.argv[3]: minTime in format time.time()
    sys.argv[4]: maxTime in format time.time()
    """
    self_dir = get_script_dir()
    os.chdir(self_dir)
    conf = parse_config(config_file)

    try:
        dirName = sys.argv[1]
        if not(os.path.isdir(dirName)):
            print('dir does not exist')
            raise TypeError
        fileType = sys.argv[2]
        if(len(sys.argv) > 5):
            print('too more arguements')
            raise Exception
        if(len(sys.argv) > 3):
            minTime = time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime(eval(sys.argv[3])))
        if(len(sys.argv) > 4):
            maxTime = time.strftime('%Y-%m-%d-%H-%M-%S', time.gmtime(eval(sys.argv[4])))
    except Exception as err:
        print("usage: ./get_data_amount.py dirName dataType [minTime] [maxTime]")
        print('##dataAmount##0##')
        sys.exit()

    os.chdir(dirName)
    if('loi' == fileType):
        _list = glob.glob('*%s' % ('blobproto'))
    elif('video' == fileType):
        _list = glob.glob('*%s' % ('3gp'))
    elif('install' == fileType):
        _list = glob.glob('*%s' % ('3gp'))
    elif('wifi' == fileType):
        _list = glob.glob('*%s' % ('tbl'))
    else:
        _list = []

    regex = re.compile(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}')

    dataAmount = 0
    for ln in _list:
        if(3 < len(sys.argv)):
            if('loi' == fileType):
                m = regex.search(ln)
                _timeStr = m.group()
            elif('video' == fileType):
                m = regex.search(ln)
                _timeStr = m.group()
            elif('install' == fileType):
                m = regex.search(ln)
                _timeStr = m.group()
            elif('wifi' == fileType):
                m = regex.search(ln)
                _timeStr = m.group()
        if(3 == len(sys.argv)):
            dataAmount += os.path.getsize(ln)
        elif(4 == len(sys.argv)) and (_timeStr >= minTime):
            dataAmount += os.path.getsize(ln)
        elif(5 == len(sys.argv)) and (_timeStr >= minTime) and (_timeStr <= maxTime):
            dataAmount += os.path.getsize(ln)

    # report
    print('##dataAmount##%s##' % (dataAmount / 1000))
