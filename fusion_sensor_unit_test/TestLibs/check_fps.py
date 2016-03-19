#!/usr/bin/env python

import os
import sys
import re
import time
import interact
import pexpect
import json
from optparse import OptionParser

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

def parse_option_args():
    # parse the options
    parser = OptionParser()
    parser.add_option("-d", "--devName", help="target devicei name")

    (options, args) = parser.parse_args()
    devName = options.devName

    return devName

if __name__ == "__main__":
    USAGE_STR = """python check_fps.py -d 8600066"""
    DEV_NAME = parse_option_args()
    CONF = parse_config(config_file)
    if (None == DEV_NAME):
        print(USAGE_STR)
        sys.exit(1)

    DEV_NAME_REGEX = re.compile(r'([1-9]{2})0{2,4}([1-9]\d{0,2})')
    M = DEV_NAME_REGEX.match(DEV_NAME)
    if (None == M):
        print(USAGE_STR)
        sys.exit(1)
    else:
        DEV_VPN_IP = "192.168.%s.%s" % (M.group(1), M.group(2))
        SSH_DEV_PROC = pexpect.spawn("ssh -p 443 root@%s" % DEV_VPN_IP)
        interact.wait_server(CONF, SSH_DEV_PROC, 'node')
        SSH_DEV_PROC.sendline("logcat -v time -d | grep FpsMeter | tail -1")
        interact.wait_server(CONF, SSH_DEV_PROC, 'node')
        print(SSH_DEV_PROC.before.split('\n')[1])
        SSH_DEV_PROC.close(force=True)
