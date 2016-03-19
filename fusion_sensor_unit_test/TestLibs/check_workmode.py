#!/usr/bin/env python
# created by Yifei.Fu at 2015-01-21

import os
import sys
import pexpect
import time
import tempfile
import json

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
    """check specified node's module status from vpn server"""
    conf = parse_config(config_file)
    from interact import *

    # TODO

    # report
    print('check module health successful.\n')
