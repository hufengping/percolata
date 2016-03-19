#!/usr/bin/env python

import os
import sys
import time
import random
import pexpect
from optparse import OptionParser

def parse_option_args():
    # parse the options
    parser = OptionParser()
    parser.add_option("-t", "--times", help="restart $times with specified intervali, default 1000 times")

    (options, args) = parser.parse_args()
    times = options.times

    if(None == times):
        times = 1000

    return (times)

if __name__ == "__main__":
    USAGE_STR = """python reset_fs.py [-t times]"""
    (_TIME) = parse_option_args()
    try:
        TIME = int(_TIME)
    except ValueError as err:
        print(err)
        print(USAGE_STR)
        sys.exit(1)

    else:
        while(TIME > 0):
            pexpect.run("adb shell am force-stop com.baysensors.FusionSensor")
            time.sleep(2)
            pexpect.run("adb shell am start -n com.baysensors.FusionSensor/com.baysensors.embedded.os.android.fusionsensor.FusionSensor")
            time.sleep(random.randint(9,30))
            TIME -= 1
