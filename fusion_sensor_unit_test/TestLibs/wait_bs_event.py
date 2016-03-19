#!/usr/bin/env python
# created by Yifei.Fu at 2015-04-13

import os
import sys
import pexpect
import time
import inspect
import json
import glob
import re
from interact import *
from optparse import OptionParser
config_file = './config_test.json'


def parse_option_args():
    # parse the options
    parser = OptionParser()
    parser.add_option("-e", "--regex", help="The target expression, in format re.")
    parser.add_option("-t", "--duration", help="Time threshold in seconds. By default it is 150s")
    parser.add_option(
        "-d",
        "--device",
        help="The device to be monitored. By default it is 1st device")
    (options, args) = parser.parse_args()
    regex = options.regex
    duration = options.duration
    device = options.device
    if regex is None:
        print("target String should be specified with '-e' option")
        sys.exit(1)
    if duration is None:
        duration = 150
    if device is None:
        device = '1st'

    return (regex, duration, device)


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
    """ wait for specified BaySensors Event on device.
    """
    self_dir = get_script_dir()
    os.chdir(self_dir)
    conf = parse_config(config_file)

    (regex, duration, devSeq) = parse_option_args()
    regEx = re.compile(regex)
    deadLine = time.time() + int(duration)

    ssh_log_proc = pexpect.spawn('bash')
    wait_server(conf, ssh_log_proc, 'vpn')
    ssh_log_proc.sendline('ssh -p 443 %s' % (conf['nodes'][devSeq]['ssh']))
    wait_server(conf, ssh_log_proc, 'node')

    ssh_log_proc.sendline('logcat -c')
    wait_server(conf, ssh_log_proc, 'node')
    ssh_log_proc.sendline('logcat -s "BaySensors":*')
    while(True):
        ssh_log_proc.expect('\r\n')
        if not (None == regEx.search(ssh_log_proc.before)):
            print("Target locate success.")
            print(ssh_log_proc.before)
            ssh_log_proc.close(force=True)
            sys.exit(0)
        elif time.time() >= deadLine:
            print("Target locate failure with timeout.")
            ssh_log_proc.close(force=True)
            sys.exit(1)
        else:
            continue
