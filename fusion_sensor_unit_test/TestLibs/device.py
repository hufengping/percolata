#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
_____________________________________________________________________________
Update Record:
    2015-12-16: Adjust the test framework for FusionSensor2.0 with new data
                pipeline.

_____________________________________________________________________________
 * BAY SENSORS INC CONFIDENTIAL
 *
 *
 *  Copyright [2012] - [2014] Bay Sensors Inc
 *  All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Bay Sensors Inc.
 * The intellectual and technical concepts contained herein are proprietary
 * to Bay Sensors Inc., and may be covered by U.S. and Foreign Patents,
 * or disclosed and claimed in pending patent applications, and are protected
 * by trade secret or copyright law.
 * Dissemination of this information or reproduction of this material is
 * strictly forbidden unless prior written permission is obtained from
 * Bay Sensors Inc.
_____________________________________________________________________________
 * @author:  yifei.fu@baysensors.com
 * @version: 2015年 12月 17日 星期四 10:03:32 CST

"""

import re
import os
import time
import pexpect
import json
import boto
import hashlib
import requests

class Device(object):
    """ Device """
    PROMPT_STR = r"(?im)root@falcon_cdma:.*#" +\
            r"|.{4}jenkins@jiri-test-machine-clone.*\$" +\
            r"|^[^\r\n]*\$"

    PSWD = r"cp4eyestalks"
    DEV_HOME_DIR = r"/data/data/berserker.android.apps.sshdroid/home/"
    INIT_RSSH_FLAG = False

    def __init__(self, name="8600176"):
        self.PlacementID = name
        self.rSshPort = self.getRSshPort(name)
        self.mergeDict = lambda d1, d2: {k: d1[k] if not k in d2
                                    else mergeDict(d1[k], d2[k]) if (k in d1 and
                                        type(d1[k]).__name__ == 'dict' and
                                        type(d2[k]).__name__ == 'dict')
                                        else d2[k] for k in set(d1) | set(d2)}
        self.executor = pexpect.spawn('bash')
        self.wait_server()
        self.mkdir('tmpDirForTest')

    def getRSshPort(self, name):
        regex = re.compile(r'\d{1}(\d{1})0{2,4}(\d{1,3})')
        m = regex.match(name)
        return("1%s%s" % (m.group(1), m.group(2)))

    def initRSsh(self):
        """initial the revert ssh tunnel to device"""
        print("Begin to initRSsh...")
#       self.executor.close(force=True)
#       self.executor = pexpect.spawn('bash')
        self.executor.sendcontrol('c')
        self.wait_server()
        self.executor.sendline("sudo netstat -anp|grep %s" % (self.rSshPort))
        self.wait_server()
        regex = re.compile(r'(?im)^\s*tcp.*127\.0\.0\.1:%s.*(?<=\s)(\d+)/sshd.*$'\
                % (self.rSshPort))
        m = regex.search(self.executor.before)
        if m is None:
            self.executor.sendline("sudo /etc/init.d/ssh restart")
        else:
            self.executor.sendline("kill -9 %s" % m.group(1))
        self.wait_server()

        _counter = 7
        while(_counter > 0):
            time.sleep(30)
            if self.isRSshEnabled():
                print("initRSsh successed.")
                self.INIT_RSSH_FLAG = True
                break
            elif _counter > 1:
                _counter -= 1
                continue
            else:
                raise RuntimeError("initRSsh failed")

    def isRSshEnabled(self):
        """check whether the revert ssh tunnel to device is created """
        self.executor.sendline("ss -ant|grep %s" % self.rSshPort)
        self.wait_server()
        regex = re.compile(r'(?im)^\s*LISTEN.*127\.0\.0\.1:%s.*$'\
                % self.rSshPort)
        m = regex.search(self.executor.before)
        if m is None:
            return False
        else:
            return True

    def runCommand(self, cmd, retry = 3):
        """
        Run shell commands on the RemoteServer
        @param cmd: the shell command shall executed on RemoteServer
        @param retry: retry times while network to device is unreachable, default by 3 times
        """
        _retry = retry
        #print("runCommand: with retry times is " + str(retry))
        #print('ssh -p %s root@localhost "%s"' % (self.rSshPort, cmd))
        self.executor.sendline('ssh -p %s root@localhost "%s"' % (self.rSshPort, cmd))
        try:
            self.wait_server()
        except RuntimeError as e:
            if e.message == "TIMEOUT" :
                self.initRSsh()
                return self.runCommand(cmd, _retry - 1)
            else:
                raise e
        finally:
            pass

        regex1 = re.compile(r'(?im)^.*(sh|scp):.*not found\s*$')#sh: command: not found
        regex2 = re.compile(r'(?im)^.*(sh|scp):.*network is unreachable.*$')#ssh: Network is unreachable
        regex3 = re.compile(r'(?im)^.*(sh|scp):.*time.{0,3}out.*$')#ssh: Connection timed out
        regex4 = re.compile(r'(?im)^.*(sh|scp):.*')#TODO
        if not regex1.search(self.executor.before) is None:
            raise NotImplementedError("command not supported by remote device.")
        elif not regex2.search(self.executor.before) is None:
            if _retry >= 1:
                if not self.INIT_RSSH_FLAG :
                    self.initRSsh()
                time.sleep(31)
                return self.runCommand(cmd, _retry - 1)
            else:
                raise IOError("Cannot access device, network is unreachable")
        elif not regex3.search(self.executor.before) is None:
            if _retry >= 1:
                time.sleep(30)
                return self.runCommand(cmd, _retry - 1)
            else:
                raise RuntimeError("Connecting device timed out")
        else:
            return self.executor.before

    def getUptime(self):
        ret = self.runCommand('uptime')
        regex = re.compile(r'(?im)^.*up\s*time: (?:(\d+) days, )?(\d{2}:\d{2}:\d{2}).*$')
        m = regex.search(ret)
        if m is None:
            raise RuntimeError("getUptime failed")
        else:
            return ("%sdays-%s"%("0" if m.group(1) is None else m.group(1), m.group(2)))

    def rebootDevice(self):
        _uptimeBefore = self.getUptime()
        self.runCommand('reboot')
        time.sleep(90)
        _uptimeAfter = self.getUptime()

        if _uptimeAfter > _uptimeBefore:
            raise RuntimeError("rebootDevice failed")
        return

    def restartFS(self):
        """restart FusionSensor on the device"""
        self.runCommand('am force-stop com.percolata.fusionsensor')
        time.sleep(3)
        self.runCommand(
                'am start -n com.percolata.fusionsensor/com.percolata.fusionsensor.FusionSensor')
        #TODO check


    def getFSVersion(self):
        """get version of FusionSensor"""
        ret = self.runCommand('cat /sdcard/VersionControl/FusionSensor')
        regex = re.compile(r'(?im)\d\.\d-\w+-R\d{2}')
        m = regex.search(ret)
        if m is None:
            return ""
        else:
            return m.group()

    def getFAVersion(self):
        """get version of FusionAdmin"""
        ret = self.runCommand('cat /sdcard/VersionControl/FusionAdmin')
        regex = re.compile(r'(?im)\d\.\d-\w+-R\d{2}')
        m = regex.search(ret)
        if m is None:
            return ""
        else:
            return m.group()

    def getWifiInfo(self):
        """
        @return: a dict includes wificonnection info
        e.g.
        {'SupplicantState': 'COMPLETED', 'MAC': '14:1a:a3:d6:83:dd', 'SSID': 'hfp_wifi', 'BSSID': '00:0f:13:40:21:82',
        'RSSI': '-64'}
        """
        ret = self.runCommand('dumpsys wifi | grep SSID')
        regex = re.compile(r'(?im)^\s*mWifiInfo:\s*\[SSID:\s*(.+?),'\
                + r'\s*BSSID:\s*(\w{2}(?::\w{2}){5}),'\
                + r'\s*MAC:\s*(\w{2}(?::\w{2}){5}),'\
                + r'\s*Supplicant state:\s*(\w*),'\
                + r'\s*RSSI:\s*(-?\d+),'\
                + r'.*\].*$')

        m = regex.search(ret)
        if m is None:
            return None
        else:
            d = dict()
            d['SSID'] = m.group(1)
            d['BSSID'] = m.group(2)
            d['MAC'] = m.group(3)
            d['SupplicantState'] = m.group(4)
            d['RSSI'] = m.group(5)
            return d

    def getCpuUsage(self):
        """
        @return: a dict includes cpu usage info
        e.g.
        {
            'load': ['18.09', '18.19', '18.09'],
            'FSUsage': {
                'overall': '8.7',
                'user': '6.1',
                'kernel': '2.5',
                'pid': '26828'
            },
            'FSFaults':{
                'minor': '10223',
                'major': '1'
            },
            'totalUsage':{
                'overall': '37',
                'user': '31.5',
                'kernel': '4.5',
                'iowait': '0.6',
                'softirq': '0.4'
            }
        }
        """
        REGEX_FLOAT = r"(?<=\W)\d{0,3}\.?\d{0,6}(?=\W)"
        REGEX_INT = r"(?<=\D)\d+(?=\D)"
        REGEX_FS_PKG = r"com\.percolata\.fusionsensor"
        REGEX_FAULTS = r"\s*/\s*faults:(?: (%s) minor| (%s) major| (%s) critical| %s \w+){1,3}"\
                % (REGEX_FLOAT, REGEX_FLOAT, REGEX_FLOAT, REGEX_FLOAT)

        ret = self.runCommand('su -c \'dumpsys cpuinfo\'')
        regexLoad = re.compile(r'(?im)^\s*Load:\s*(%s)\s*/\s*(%s)\s*/\s*(%s)\s*$'
                % (REGEX_FLOAT, REGEX_FLOAT, REGEX_FLOAT))
        regexFSUsage = re.compile(r'(?im)^\s*(%s)%% (%s)/%s: (%s)%% user \+ (%s)%% kernel(?:%s)?\s*$'
                % (REGEX_FLOAT, REGEX_INT, REGEX_FS_PKG,
                REGEX_FLOAT, REGEX_FLOAT, REGEX_FAULTS))
        regexTotalUsage = re.compile(r'(?im)^\s*(%s)%% TOTAL: (%s)%% user \+ (%s)%% kernel'
                % (REGEX_FLOAT, REGEX_FLOAT, REGEX_FLOAT) +
                r'(?: \+ (%s)%% iowait)? \+ (%s)%% softirq\s*$'
                % (REGEX_FLOAT, REGEX_FLOAT))

        m1 = regexLoad.search(ret)
        m2 = regexFSUsage.search(ret)
        m3 = regexTotalUsage.search(ret)
        if m1 is None or m2 is None or m3 is None:
            raise RuntimeError("extracting cpu usage info from \"%s\" failed"%ret)
        else:
            d = dict()
            d['load'] = [m1.group(1), m1.group(2), m1.group(3)]
            d['FSUsage'] = {'overall':m2.group(1), 'pid':m2.group(2), \
                    'user':m2.group(3), 'kernel':m2.group(4)}
            d['FSFaults'] = {'minor':m2.group(5), 'major':m2.group(6), 'critical':m2.group(7)}
            d['totalUsage'] = {'overall':m3.group(1), 'user':m3.group(2), 'kernel':m3.group(3),\
                     'iowait':m3.group(4), 'softirq':m3.group(5)}

            return d

    def getMemUsage(self):
        """
        @return a dict which includes memory usage info of device.
        e.g.
        {
            'FSMemUsage': '42741', #in kB
            'totalRAM': '901616',
            'usedRAM': '369593',
            'freeRAM': '436596'
        }
        """
        REGEX_INT = r"(?<=\D)\d+(?=\D)"
        REGEX_FS_PKG = r"com\.percolata\.fusionsensor"
        regexFS = re.compile(r'(?m)^\s*(%s) kB: %s .*$'\
                % (REGEX_INT, REGEX_FS_PKG))
        regexTotal = re.compile(r'(?m)^\s*Total RAM: (%s) kB\s*$'\
                % REGEX_INT)
        regexFree = re.compile(r'(?m)^\s*Free RAM: (%s) kB .*$'\
                % REGEX_INT)
        regexUsed = re.compile(r'(?m)^\s*Used RAM: (%s) kB .*$'\
                % REGEX_INT)

        ret = self.runCommand('dumpsys meminfo')
        m1 = regexFS.search(ret)
        m2 = regexTotal.search(ret)
        m3 = regexFree.search(ret)
        m4 = regexUsed.search(ret)

        if m1 is None or m2 is None or m3 is None or m4 is None:
            raise RuntimeError("extracting memory usage info from \"%s\" failed"%ret)
        else:
            d = dict()
            d['FSMemUsage'] = m1.group(1)
            d['totalRAM'] = m2.group(1)
            d['freeRAM'] = m3.group(1)
            d['usedRAM'] = m4.group(1)
            return d

    def getSdcardUsage(self):
        """
        @return a dict which includes sdcard usage info of device.
        e.g.
        {
            'total': '5500', #in MB
            'used': '898.3',
            'free': '4600'
        }
        """
        REGEX_FLOAT = r"(?<=\W)\d{0,3}\.?\d{0,6}(?=\W)"
        regex = re.compile(r'(?im)^\s*/data\s*(%s)(G|M|K)\s*(%s)(G|M|K)\s*(%s)(G|M|K).*$'\
                % (REGEX_FLOAT, REGEX_FLOAT, REGEX_FLOAT))

        ret = self.runCommand('df')
        m = regex.search(ret)
        if m is None:
            raise RuntimeError("extracting sdcard usage info from \"%s\" failed"%ret)
        else:
            d = dict()
            d['total'] = self._unitTrans(m.group(1), m.group(2))
            d['used'] = self._unitTrans(m.group(3), m.group(4))
            d['free'] = self._unitTrans(m.group(5), m.group(6))
            return d

    def isNewDataOnDevice(self, dataType="video", timeline=time.time()-20*60):
        """check whether new generated data still on device(not uploaded yet)
        @param dataType: video|loi|zone-count|tracking|audio|wifi
        @param timeline: timestamp, data generated before that will not be count,
                         default by 20 mins ago
        Restrict: no other file exists in data file dir
        """
        timeStr = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime(timeline))

        timeRegex = re.compile(r'\d{4}(-\d{2}){5}')
        try:
            if "video" == dataType:
                dayStr = re.compile(r'\d{4}(-\d{2}){2}').search(
                        self.runCommand('busybox ls -t /sdcard/Pictures/video/ | head -1')
                        ).group()
                ret = self.runCommand(
                        'busybox ls -t /sdcard/Pictures/video/%s/ | head -1'
                        % dayStr
                        )
                return timeRegex.search(ret).group() >= timeStr
            if "loi" == dataType:
                ret = self.runCommand(
                        'busybox ls -t /sdcard/Download/ | head -1'
                        )
                return timeRegex.search(ret).group() >= timeStr
            if "zone-count" == dataType:
                ret = self.runCommand(
                        'busybox ls -t /sdcard/ZoneCount/ | head -1'
                        )
                return timeRegex.search(ret).group() >= timeStr
            if "tracking" == dataType:
                ret = self.runCommand(
                        'busybox ls -t /sdcard/Tracking/ | head -1'
                        )
                return timeRegex.search(ret).group() >= timeStr
            if "wifi" == dataType:
                ret = self.runCommand(
                        'busybox ls -t /sdcard/BS-wifi/ | head -1'
                        )
                return timeRegex.search(ret).group() >= timeStr
            if "audio" == dataType:
                ret = self.runCommand(
                        'busybox ls -t /sdcard/Audio/ | head -1'
                        )
                return timeRegex.search(ret).group() >= timeStr
            if "install" == dataType:
                dayStr = re.compile(r'\d{4}(-\d{2}){2}').search(
                        self.runCommand('busybox ls -t /sdcard/Pictures/install/ | head -1')
                        ).group()
                ret = self.runCommand(
                        'busybox ls -t /sdcard/Pictures/install/%s/ | head -1'
                        % dayStr
                        )
                return timeRegex.search(ret).group() >= timeStr
        except AttributeError as e:
            return False


    def _unitTrans(self, num, unit):
        """
        @param num: str, denote quantity value
        @param unit: str, denote original unit, may be G|M|K
        @return str value denote transformed size in MB
        """
        if unit == 'G':
            return str(float(num)*1000)
        elif unit == 'M':
            return num
        elif unit == 'K':
            return str(float(num)/1000)
        else:
            raise ValueError("Unkown unit: %s" % unit)

    def getLocalCfg(self):
        """get local fusion-sensor config file on device
        @return a dict form config
        """
        self.download("/sdcard/fusion-sensor.json", "./tmp-local-cfg.json")
        with open("./tmp-local-cfg.json", 'rb') as config:
            cfg = json.load(config)
            return cfg

    def setLocalCfg(self, newCfg):
        """set local fusion-sensor config file on device
        @param newCfg: new device config items in json form
        e.g.
        {
            "PlacementID": "8600067",
            "hostname": "https://phone:11222011@api.percolata.com",
            "softwareUpdate": {
                "updateURL": "https://phone:11222011@api.percolata.com"
            },
            "WifiAccess": {
                "1": {
                    "SSID": "Percolata-2G",
                    "hiddenSSID": "no",
                    "key": "&*^@374"
                }
            },
            "AccessList": [
                "1"
            ]
        }
        """
        oldCfg = self.getLocalCfg()
        _cfg = self.mergeDict(oldCfg, newCfg)

        with open("./tmp-local-cfg.json", 'wb') as config:
            config.truncate()
            json.dump(_cfg, config, indent=4, separators=[',', ';'], sort_keys=True)

        self.upload("./tmp-local-cfg.json", "/sdcard/fusion-sensor.json")

    def getDevCfg(self):
#TODO Modification after migrate to microsoft cloud
        """get device config file from google storage, need config .boto in users' home dir
        @return a dict form config
        """
        hostname = self.getLocalCfg()['hostname']
        gs_conn = boto.connect_gs()
        if hostname.__contains__("ci-api"):
            bucket = gs_conn.get_bucket("percolata-test")#T_T
        elif hostname.__contains__("api"):
            bucket = gs_conn.get_bucket("percolata-data")
        else:
            raise NotImplementedError("cannot get config from %s yet" % hostname)
        key = bucket.get_key(r"config/%s.json" % self.PlacementID)
        devCfg = json.loads(key.get_contents_as_string())
        return devCfg

    def setDevCfg(self, newCfg):
        """set device config file on google storage, need config .boto in users' home dir
        @param newCfg: new device config items in json form
        e.g.
        {
            "PlacementID": "8600067",
            "hostname": "https://phone:11222011@api.percolata.com",
            "softwareUpdate": {
                "updateURL": "https://phone:11222011@api.percolata.com"
            },
            "WifiAccess": {
                "1": {
                    "SSID": "Percolata-2G",
                    "hiddenSSID": "no",
                    "key": "&*^@374"
                }
            },
            "AccessList": [
                "1"
            ]
        }
        """
        hostname = self.getLocalCfg()['hostname']
        gs_conn = boto.connect_gs()
        if hostname.__contains__("ci-api"):
            bucket = gs_conn.get_bucket("percolata-test")#T_T
            url = "https://ci-api.percolata.com/modify_config"#WARN: write IP inline
        elif hostname.__contains__("api"):
            bucket = gs_conn.get_bucket("percolata-data")
            url = "https://config.percolata.com/modify_config"
        else:
            raise NotImplementedError("cannot get config from %s yet" % hostname)
        key = bucket.get_key(r"config/%s.json" % self.PlacementID)
        oldDevCfg = json.loads(key.get_contents_as_string())
        newDevCfg = self.mergeDict(oldDevCfg, newCfg)

        with open("./tmp_dev_cfg.json","wb+") as cfg:
            json.dump(newDevCfg, cfg, indent=4, separators=[',', ':'], sort_keys=True)
            cfg.flush()
            cfg.seek(0)
            md5 = getMD5(cfg.read())
            cfg.seek(0)
            r = requests.post(
                    url,
                    auth=('phone', '11222011'),
                    headers={'HOST': 'config.percolata.com'},
                    data={
                        'placement_name': self.PlacementID,
                        'file_name': self.PlacementID + '.json',
                        'md5': md5},
                    files={'file': cfg},
                    verify=False
                    )
            if not r.status_code == 200:
                raise RuntimeError("Failed to modify config with: %s" % r.content)


    def getChecksum(self, fileDir):
        """get the checksum of local file on device.
        @param fileDir: the file dirpath on device
        """
        ret = self.runCommand("md5sum %s" % fileDir)
        regex = re.compile(r'(?im)^\s*([0-9a-f]{32})\s+.*$')

        m = regex.search(ret)
        if m is None:
            raise RuntimeError("get chksum failed: %s" % ret)
        else:
            return m.group(1)

    def isFSRunning(self):
        """
        check whether the FusionSensor on device is running.
        """
        REGEX_FS_PKG = r"com\.percolata\.fusionsensor"

        ret = self.runCommand("ps |grep percolata")
        regex = re.compile(REGEX_FS_PKG)

        m = regex.search(ret)
        if m is None:
            return False
        else:
            return True

    def getLogcat(self):
        """get logcat msg, currently there are not many useful info as too many redundant info."""
        ret = self.runCommand("logcat -v time -d |grep -E \"Android|Activity|Percolata\" |grep -vE \"framePool\"")
        return ret

    def upload(self, srcDir, dstDir='tmpDirForTest'):
        """
        Upload local files or dirs to device
        @param srcDir: local file or dir
        @param dstDir: remote dir
        for convenience, will not check size of srcDir, clients should note that.
        """
        if os.path.exists(srcDir):
            if os.path.isfile(srcDir):
                self.executor.sendline('scp -P %s %s root@localhost:tmpDirForTest' \
                        % (self.rSshPort, srcDir))
                self.wait_server(600)
            elif os.path.isdir(srcDir):
                self.executor.sendline('scp -r -P %s %s root@localhost:tmpDirForTest' \
                        % (self.rSshPort, srcDir))
                self.wait_server(600)
            else:
                raise ValueError("Wrong srcDir type: %s" % srcDir)
            if not self.isDirExists('tmpDirForTest/%s' % srcDir):
                raise RuntimeError("Failed to upload local dir to RemoteServer")
            elif 'tmpDirForTest' != dstDir:
                self.runCommand("su -c 'cp -r %s/tmpDirForTest/%s %s'"\
                        % (self.DEV_HOME_DIR, srcDir, dstDir))
        else:
            raise IOError("srcDir is not exist")

    def download(self, srcDir, dstDir='.'):
        """
        Download files or dirs from device
        @param srcDir: remote file or dir
        @param dstDir: local dir
        """
        if not self.isDirExists(srcDir):
            raise IOError("srcDir is not exist")

        self.executor.sendline('scp -rP %s root@localhost:%s %s' \
                % (self.rSshPort, srcDir, dstDir))
        self.wait_server(600)

    #Client should notice permission issue, suggest creating new dir in user's home dir.
    def mkdir(self, dirname):
        self.runCommand(r'mkdir %s' % dirname)
        if not self.isDirExists(dirname):
            raise IOError("Failed to mkdir %s" % dirname)

    def rmdir(self, dirname):
        self.runCommand(r'rm -rf %s' % dirname)
        if self.isDirExists(dirname):
            raise IOError("Failed to rmdir %s" % dirname)

    def isDirExists(self, dirname):
        ret = self.runCommand(r'if [ -e %s ];then echo remoteDirExist ;fi' % dirname)
        regex = re.compile(r'(?m)^\s*remoteDirExist\s*$')
        if not regex.search(ret) is None:
            return True
        else:
            return False

    def wait_server(self, timeout=60):
        switch = self.executor.expect([self.PROMPT_STR,
                    pexpect.EOF,
                    pexpect.TIMEOUT,
                    r"assword:",
                    r"\(yes/no\)\?"],
                    timeout
                )
        if 0 == switch:
            return
        elif 1 == switch:
            raise EOFError("EOFError")
        elif 2 == switch:
            raise RuntimeError("TIMEOUT")
        elif 3 == switch:
            self.executor.sendline(self.PSWD)
            self.wait_server(timeout)
        elif 4 == switch:
            self.executor.sendline('yes')
            self.wait_server(timeout)
        else:
            raise Exception("UnkownError")

    def close(self):
        self.rmdir('tmpDirForTest')
        self.executor.close(force=True)

def getMD5(content, system="hex"):
    """
    Args:
        content: content to be added md5
    Return:
        md5 string
    """
    m = hashlib.md5()
    m.update(content)
    if system == 'hex':
        return m.hexdigest()
    else:
        return m.digest()
#end of class Device

