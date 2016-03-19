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
    """check specified node's healthy status from vpn server"""
    conf = parse_config(config_file)
    from interact import *

    c = pexpect.spawn('bash')
    c.sendline('ssh -p 443 %s' % (conf['nodes']['1st']['ssh']))
    wait_server(conf, c, 'node')

    # check free mem
    c.sendline("free |head -2 |tail -1| awk '{print $4}'")
    wait_server(conf, c, 'node')

    # ....block>>>>if free mem less then 80M, then raise error
    if(10000 > eval(c.before.split()[-1])):
        print('check free mem failure.\n')
        raise Exception("check free mem failure.")

    # check iostat
    c.sendline("iostat | head -4 | tail -1")
    wait_server(conf, c, 'node')

    # iostat  %user   %nice %system %iowait  %steal   %idle
    l = c.before.split()[-6:-1]
    if(eval(l[0]) > 90.00):
        print('==failure==: user cpu usage > 90 \n')
        raise Exception("user cpu usage > 90.")
    if(eval(l[2]) > 40.00):
        print('==failure==: system cpu usage > 40 \n')
        raise Exception("system cpu usage > 40.")
    if(eval(l[4]) > 8.00):
        print('==failure==: steal cpu usage > 8 \n')
        raise Exception("steal cpu usage > 8.")

    if(eval(l[0]) > 80.00):
        print('==warn==: user cpu usage > 80 \n')
    if(eval(l[2]) > 30.00):
        print('==warn==: system cpu usage > 30 \n')
    if(eval(l[4]) > 0.00):
        print('==warn==: steal cpu usage > 0 \n')

    # succeeded
    print('check node healthy successful.\n')
