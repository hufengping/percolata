#!/usr/bin/env python
# created by Yifei.Fu at 2015-04-01

import os
import sys
import time
import re
import pexpect
import json
import inspect
config_file = './config_test.json'
# list of devices


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
        raise Exception("undefined exception.")

    return configurations
# end of parse_config


def getDevIP(devName):
    """"""
    regex = re.compile(r'([1-9]{2})0{2,4}([1-9]\d{0,2})')
    m = regex.match(devName)
    if(None != m):
        return "192.168.%s.%s" % (m.group(1), m.group(2))
    else:
        return None
# end of getDevIP


def getDevConf(testConf, devName):
    """"""
    ipAddr = getDevIP(devName)
    devConfFileName = '%s_runtime.json' % devName
    c = pexpect.spawn('sh')
    wait_server(testConf, c, 'vpn')

    curTime = time.time()
    c.sendline("scp -P 443 root@%s:/sdcard/fusion-sensor.json ./%s" % (ipAddr, devConfFileName))
    try:
        wait_server(testConf, c, 'vpn')
    except Exception as err:
        return None
    if (os.path.isfile(devConfFileName) and (curTime < os.path.getmtime(devConfFileName))):
        devConf = parse_config(devConfFileName)
        c.sendline("rm -f %s" % devConfFileName)
        wait_server(testConf, c, 'vpn')
        return devConf
    else:
        return None
# end of getdevconf


def get_curlRate(conf, devName):
    ipAddr = getDevIP(devName)

    ssh_curl_proc = pexpect.spawn('sh')
    wait_server(conf, ssh_curl_proc, 'vpn')

    ssh_curl_proc.sendline("scp -P 443 curl.zip root@%s:/data/" % ipAddr)
    wait_server(conf, ssh_curl_proc, 'vpn', 200)
    ssh_curl_proc.sendline("ssh -p 443 root@%s" % ipAddr)
    wait_server(conf, ssh_curl_proc, 'node')
    ssh_curl_proc.sendline("cd /data;busybox unzip -qo curl.zip")
    wait_server(conf, ssh_curl_proc, 'node')
    ssh_curl_proc.sendline("mkdir /sdcard/TestBench;cd /sdcard/TestBench")
    wait_server(conf, ssh_curl_proc, 'node')
    ssh_curl_proc.sendline("busybox dd if=/dev/zero bs=1M count=2 of=./%s_BW_Calc" % devName)
    wait_server(conf, ssh_curl_proc, 'node')
    import random
    newvalue = random.randint(0, 65535) + int(time.time())
    ssh_curl_proc.sendline("echo %s >> %s_BW_Calc" % (newvalue, devName))
    wait_server(conf, ssh_curl_proc, 'node')
    ssh_curl_proc.sendline("md5sum %s_BW_Calc" % devName)
    wait_server(conf, ssh_curl_proc, 'node')
    md5Value = ssh_curl_proc.before.split()[-2]

    startTime = time.time()
    ssh_curl_proc.sendline(
        r"curl -k -H 'Expect:' -F 'file=@%s_BW_Calc' -i %svideo_file?id=%s\&filename=%s_BW_Calc\&md5=%s" %
        (devName, conf['uploadURL'], devName, devName, md5Value))
    try:
        wait_server(conf, ssh_curl_proc, 'node', 3600)
    except Exception as err:
        if('TIMEOUT' == err.message):
            pexpect.run(
                "bash -c \"echo '===%s===: upload rate beneath lower limit' >> BW_record\"" %
                devName)
        else:
            pexpect.run("bash -c \"echo '===%s===: Abortion' >> BW_record\"" % devName)
        raise Exception(err)

    if ssh_curl_proc.before.find('"status":"ok"') == -1:
        pexpect.run("bash -c 'echo Http failue with %s >> BW_log'" % devName)
        raise Exception("Http failure")

    endTime = time.time()

    ssh_curl_proc.close(force=True)
    return (2 * 1024 / (endTime - startTime), startTime, endTime)
# end of get_curlRate


def get_dataRate(testConf, hostname, devName, startTime, endTime):
    dataAmount = 0
    # login to vpn,dp
    ssh_dp_proc = pexpect.spawn("ssh deployer@%s" % hostname)
    wait_server(testConf, ssh_dp_proc, 'dp')
    ssh_dp_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    wait_server(testConf, ssh_dp_proc, 'dp')

    ssh_data_proc = pexpect.spawn('sh')
    wait_server(testConf, ssh_data_proc, 'vpn')
    ssh_data_proc.sendline("scp get_data_amount.py deployer@%s:~/TestBench/" % hostname)
    wait_server(testConf, ssh_data_proc, 'vpn')
    ssh_data_proc.sendline("scp config_test.json deployer@%s:~/TestBench/" % hostname)
    wait_server(testConf, ssh_data_proc, 'vpn')
    ssh_data_proc.sendline("scp interact.py deployer@%s:~/TestBench/" % hostname)
    wait_server(testConf, ssh_data_proc, 'vpn')
    ssh_data_proc.close(force=True)

    ssh_dp_proc.sendline(r"python ~/TestBench/get_data_amount.py %s wifi %s %s" %
                         (os.path.join(testConf['svr_wifi_dir'], devName), str(startTime), str(endTime)))
    wait_server(testConf, ssh_dp_proc, 'dp')
    tmpList = ssh_dp_proc.before.split('##')
    dataAmount += int(tmpList[tmpList.index('dataAmount') + 1])
    ssh_dp_proc.sendline(r"python ~/TestBench/get_data_amount.py %s video %s %s" %
                         (os.path.join(testConf['svr_video_dir'], devName), str(startTime), str(endTime)))
    wait_server(testConf, ssh_dp_proc, 'dp')
    tmpList = ssh_dp_proc.before.split('##')
    dataAmount += int(tmpList[tmpList.index('dataAmount') + 1])
    ssh_dp_proc.close(force=True)
    return (dataAmount / (endTime - startTime))
# end of get_dataRate

if __name__ == '__main__':
    """
    sys.argv[1]: devName of the target device"""
    self_dir = get_script_dir()
    os.chdir(self_dir)

    devName = sys.argv[1]
    testConf = parse_config(config_file)
    from interact import *
    devConf = getDevConf(testConf, devName)
    hostname = devConf['hostname'].split('@')[1]
    curlRate, startTime, endTime = get_curlRate(testConf, devName)
    dataRate = get_dataRate(testConf, hostname, devName, startTime, endTime)

    pexpect.run(
        "bash -c \"echo '===%s=== curlRate: %s KBps  |  dataRate: %sKBps' >> BW_record\"" %
        (devName, curlRate, dataRate))
    print("calculate success.")
