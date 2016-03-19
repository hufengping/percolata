#!/usr/bin/env python
# created by Yifei.Fu at 2015-01-21

import os
import sys
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
    """check specified node's module status from dp server"""
    conf = parse_config(config_file)
    from interact import *
    from time import *
    from pexpect import *
    devName = sys.argv[1]  # get placement name from argv
    expMode = eval(sys.argv[2])

    _myNo = get_dp_no(conf)
    if (_myNo is None):
        print("get dp no failure: unknown dp server.\n")
        raise Exception("unknown dp server.")

    index = -1
    heartbeat = str()
    with open('/log/placement_%s.txt'%devName,'r') as logFile:
        lineList = logFile.readlines()
        while(True):
            if not(lineList[index].__contains__('FS-status')):
                index -= 1
                continue
            else:
                heartbeat = lineList[index].strip()
                break
    statusList = heartbeat.split('|')

    for item in expMode:
        try:
            if(item == 'log'):
                # we say, the log module == ok when its latest heartbeat came later than
                # 20min at past.
                time_lim = strftime('%Y-%m-%d %H:%M:%S', gmtime(time() - 1200))
                index = statusList.index('FS-status')
                time_rcv = statusList[index - 2]
                print(time_rcv, time_lim)
                if(time_rcv < time_lim):
                    print('check log module failure.\n')
                    raise Exception("check log module failure.")
            elif(item == 'config'):
                # TODO
                pass
            elif(item == 'upload'):
                # TODO improvement
                # currently, check left list has no less than 2 zeros, e.g. "Left:1*0*0*0"
                index = statusList.index('BS-uploader')
                tag = statusList[index + 1].split(',')[0].split(':')[1].split('*')
                count = 0
                for e in tag:
                    if(e == '0'):
                        count += 1
                if(count <= 1):
                    print('check upload module failure.\n')
                    raise Exception("check upload module failure.")
            elif(item == 'upgrade'):
                index = statusList.index('BS-update')
                tag = statusList[index + 1].split()
                for k, v in expMode[item].items():
                    if(k == 'updateTime'):
                        if not((tag[1] == v)):
                            print('check upgrade module mode failure.\n')
                            raise Exception("check upgrade module mode failure.")
                    else:  # TODO
                        pass
            elif(item == 'sysmon'):
                pass
#               index = statusList.index('BS-sysmon')
#               tag = statusList[index+1]
#               if not(tag[0] == 'C'):
#                   print('check sysmon module failure.\n')
#                   raise Exception("undefined exception.")
            elif(item == 'video'):
                index = statusList.index('BS-video')
                tag = statusList[index + 1].split()
                for k, v in expMode[item].items():
                    if(k == 'mode'):
                        if not((tag[0] == v)):
                            print('check video module mode failure.\n')
                            raise Exception("check video module mode failure.")
                    elif(k == 'state'):
                        print(tag)
                        if (v == 'STATE_STARTED') and (tag[2] == v):
                            continue
                        elif (v == 'STATE_SLEEP') and (tag[3] == 'sleeping'):
                            continue
                        else:
                            print('check video module mode failure.\n')
                            raise Exception("check video module mode failure.")
                    else:  # TODO
                        pass
            elif(item == 'wifi'):
                index = statusList.index('BS-wifi')
                tag = statusList[index + 1].split()
                if not(tag[2] == "true"):
                    print('check wifi module failure.\n')
                    raise Exception("check wifi mode failure.")
            elif(item == 'wificontrol'):
                index = statusList.index('BS-wificontrol')
                tag = statusList[index + 1]
                if not(tag[0] == 'U'):
                    print('check wificontrol module failure.\n')
                    raise Exception("check wificontrol module failure.")
            elif(item == 'openvpn'):
                index = statusList.index('BS-openvpn')
                tag = statusList[index + 1]
                if not(tag == 'yes'):
                    print('check openvpn module failure.\n')
                    raise Exception("check openvpn module failure.")
            elif(item == 'websocket'):
                index = statusList.index('BS-websocket')
                tag = statusList[index + 1]
                if not(tag == 'yes'):
                    print('check module failure.\n')
                    raise Exception("check module failure.")
            else:
                # unsurported module
                pass
        except Exception as err:
            print("unexpected failure while checking heartbeat with %s : %s" % (item, err))
            raise Exception("%s."%(err))

    # report
    print('check module mode successful.\n')

    # release subprocess
