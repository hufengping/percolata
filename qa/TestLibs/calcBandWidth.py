#!/usr/bin/env python
#created by Yifei.Fu at 2015-04-01

import os,sys,time,re,pexpect
import json
config_file = './config_test.json'
#list of devices
devList = ["8100069",
        "8200011",
        "8100066",
        "8100074",
        "8200004",
        "8200026",
        "8100077",
        "8100083",
        "8200007",
        "8200015",
        "8100017",
        "8100070",
        "8200017",
        "8200020",
        "8600070",
        "8600076",
        "8100058",
        "8100086",
        "8100085",
        "8100097",
        "8100047",
        "8100055",
        "8600157",
        "8600205",
        "8100036",
        "8100039",
        "8100095",
        "8200008",
        "8200021",
        "8100056",
        "8100057",
        "8100040",
        "8100043",
        "8100045",
        "8100046",
        "8100042",
        "8100044",
        "8100051",
        "8100059",
        "8200014",
        "8100049",
        "8200005",
        "8100024",
        "8100025",
        "8100018",
        "8100019",
        "8100020",
        "8100072",
        "8100035",
        "8100054",
        "8600104",
        "8600166",
        "8100048",
        "8100071",
        "8100082",
        "8200022"
        ]

def parse_config(filename):
    configurations = {}

    try:
        with open(filename,'r') as config:
            #parse config_file
            configurations = json.load(config)
    except IOError as err:
        print('open config file failure.\n')
        raise Exception("undefined exception.")

    return configurations
#end of parse_config

def getDevIP(devName):
    """"""
    regex = re.compile(r'([1-9]{2})0{2,4}([1-9]\d{0,2})')
    m = regex.match(devName)
    if(None != m):
        return "192.168.%s.%s"%(m.group(1),m.group(2))
    else:
        return None
#end of getDevIP

def getDevConf(testConf,devName):
    """"""
    ipAddr = getDevIP(devName)
    devConfFileName = '%s_runtime.json'%devName
    c = pexpect.spawn('bash')
    wait_server(testConf,c,'vpn')

    curTime = time.time()
    c.sendline("scp -P 443 root@%s:/sdcard/fusion-sensor.json ./%s"%(ipAddr,devConfFileName))
    try:
        wait_server(testConf,c,'vpn')
    except Exception as err:
        return None
    if (os.path.isfile(devConfFileName) and (curTime < os.path.getmtime(devConfFileName))):
        devConf = parse_config(devConfFileName)
        c.sendline("rm -f %s"%devConfFileName)
        wait_server(testConf,c,'vpn')
        return devConf
    else:
        return None
#end of getdevconf

if __name__ == '__main__':
    usageStr = """
    """
    conf = parse_config(config_file)
    from interact import *

    calcSchedule = {}
    for devName in devList:
        devConf = getDevConf(conf,devName)
        if(None == devConf):
            if(calcSchedule.has_key('unavailable')):
                if not(calcSchedule[scheduleHour].__contains__(devName)):
                    calcSchedule['unavailable'].append(devName)
            else:
                calcSchedule['unavailable'] = []
                calcSchedule['unavailable'].append(devName)
        else:
            scheduleHour = (int(devConf['workHours'].split('-')[0].split(':')[0]) + 7)%24
            if(calcSchedule.has_key(scheduleHour)):
                if not(calcSchedule[scheduleHour].__contains__(devName)):
                    calcSchedule[scheduleHour].append(devName)
            else:
                calcSchedule[scheduleHour] = []
                calcSchedule[scheduleHour].append(devName)

    counter = 25
    while(counter > 0):
        print(str(calcSchedule))
        curHour = time.gmtime().tm_hour
        curMin = time.gmtime().tm_min
        if(curMin > 30):
            time.sleep((61 - curMin)*60)
            counter -= 1
            continue
        #retry formally unavailable devices
        if(calcSchedule.has_key('unavailable')):
            for devName in calcSchedule['unavailable']:
                devConf = getDevConf(conf,devName)
                if not (None == devConf):
                    scheduleHour = (int(devConf['workHours'].split('-')[0].split(':')[0]) + 7)%24
                    if(calcSchedule.has_key(scheduleHour)):
                        if not(calcSchedule[scheduleHour].__contains__(devName)):
                            calcSchedule[scheduleHour].append(devName)
                    else:
                        calcSchedule[scheduleHour] = []
                        calcSchedule[scheduleHour].append(devName)
                    calcSchedule['unavailable'].remove(devName)

        if(calcSchedule.has_key(curHour)):
            for devName in calcSchedule[curHour]:
                print("at %s %s"%(curHour,devName))
                try:
                    c = pexpect.spawn('bash')
                    c.sendline("python BW_Calculator.py %s &"%devName)
                    c.expect('\$')
                except Exception as err:
                    pexpect.run("bash -c 'echo err:%s with calculating BW for %s >> BW_log'"%(err,devName))

        curMin = time.gmtime().tm_min
        time.sleep((61 - curMin)*60)
        counter -= 1

    #TODO handle record file
    for devName in devList:
        pass
