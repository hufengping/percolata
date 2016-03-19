#!/usr/bin/env python


import os
import re
import json
import time

DEV_LIST = './dev_list'





if __name__ == "__main__":
    devList = list()
    verDict = dict()
    logRegEx = re.compile(r'\./(history-(?P<time>\d{4}-\d{2}-\d{2})/|)placement_\d{7,8}\.txt')
    verPattern = 'FS-fusion_sensor'
    with open(DEV_LIST,'r') as devFile:
        for line in devFile:
            devList.append(line.strip())
    curDir = os.getcwd()
    os.chdir('/log')
    for dev in devList:
        logList = list()
        os.system("find . -name placement_%s.txt > rec"%dev)
        with open('rec','r') as logFile:
            for log in logFile:
                logList.append(log.strip())
        logList.sort(reverse=True)
        for log in logList:
            os.system("grep -a %s %s |tail -1 > verRec"%(verPattern, log))
            with open('verRec','r') as logRec:
                verStr = logRec.readline()
                if verStr == '':
                    continue
                else:
                    _ver_info = verStr.split('|')
                    verDict[dev]={'updateTime':_ver_info[2],'version':_ver_info[4].split(',')[0].strip('@')}
                    break

    os.chdir(curDir)
    with open('version.json','w+') as outFile:
        json.dump(verDict, outFile, sort_keys=True)
