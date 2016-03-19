#!/usr/bin/env python

import os
import sys
import re
import time
import glob
import random
import pexpect
from optparse import OptionParser

def parse_option_args():
    # parse the options
    parser = OptionParser()
    parser.add_option("-t", "--dataType", help="specified data type")
    parser.add_option("-d", "--devName", help="target devicei name")

    (options, args) = parser.parse_args()
    dataType = options.dataType
    devName = options.devName

    return (dataType, devName)

if __name__ == "__main__":
    USAGE_STR = """python check_data_hole.py -t loi|video|zone-count|wifi|audio -d 8600066"""
    (DATA_TYPE, DEV_NAME) = parse_option_args()

    if 'loi' == DATA_TYPE:
        DATA_DIR = '/data/blob/dump'
    elif 'video' == DATA_TYPE:
        DATA_DIR = '/data/video/dump'
    elif 'zone-count' == DATA_TYPE:
        DATA_DIR = '/data/tripline_images/dump'
    elif 'wifi' == DATA_TYPE:
        DATA_DIR = '/data/wifi/dump'
    elif 'audio' == DATA_TYPE:
        DATA_DIR = '/data/audio/dump'
    else:
        print(USAGE_STR)
        sys.exit(1)

    DEV_NAME_REGEX = re.compile(r'([1-9]{2})0{2,4}([1-9]\d{0,2})')
    if None == DEV_NAME_REGEX.match(DEV_NAME):
        print(USAGE_STR)
        sys.exit(1)
    else:
        os.chdir(os.path.join(DATA_DIR, DEV_NAME))
        FILE_LIST = glob.glob('*')
        TIME_LIST = list()
        TIME_REGEX = re.compile(r'\d{4}(-\d{2}){5}')
        for elem in FILE_LIST:
            TIME_LIST.append(TIME_REGEX.search(elem).group())

        TIME_LIST.sort()

        MAX_DATA_HOLE = [0.0,'','']#[DELTA_TIME, PREV_TIME_STRING, CUR_TIME_STRING]
        SEC_DATA_HOLE = [0.0,'','']#[DELTA_TIME, PREV_TIME_STRING, CUR_TIME_STRING]
        TRD_DATA_HOLE = [0.0,'','']#[DELTA_TIME, PREV_TIME_STRING, CUR_TIME_STRING]
        PREV_TIME = time.mktime(time.strptime(TIME_LIST[0], '%Y-%m-%d-%H-%M-%S'))
        PREV_TIME_STRING = TIME_LIST[0]
        for ite in TIME_LIST:
            CUR_TIME = time.mktime(time.strptime(ite, '%Y-%m-%d-%H-%M-%S'))
            DELTA_TIME = CUR_TIME - PREV_TIME
            if DELTA_TIME > MAX_DATA_HOLE[0]:
                TRD_DATA_HOLE = SEC_DATA_HOLE
                SEC_DATA_HOLE = MAX_DATA_HOLE
                MAX_DATA_HOLE = [DELTA_TIME, PREV_TIME_STRING, ite]
            PREV_TIME = CUR_TIME
            PREV_TIME_STRING = ite

        print("[HOLE_DURATION, TIME_BEFORE_HOLE, TIME_AFTER_HOLE]")
        print(MAX_DATA_HOLE)
        print(SEC_DATA_HOLE)
        print(TRD_DATA_HOLE)
