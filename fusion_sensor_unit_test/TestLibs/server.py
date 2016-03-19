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
class RemoteServer(object):
    """ Remote Server
        dp0: "dp0.baysensors.com" or "software.baysensors.com"
        vpn2: "vpn2.baysensors.com"
        slave1: "jenkins@199.223.236.196"
    """
    PROMPT_STR = r"(?im)\(ENV\).{4}deployer@dp-office.*\$" +\
            r"|.{4}jenkins@jiri-test-machine-clone.*\$" +\
            r"|.{4}deployer@vpn2.*\$" +\
            r"|.{4}jolyon@jolyon-H535.*\$" +\
            r"|^[^\r\n]*\$"

    def __init__(self, host='localhost', user=None, pswd=None):
        self._host = host
        self._user = user
        self._pswd = pswd
        self.executor = pexpect.spawn('bash')
        self.wait_server()
        self.mkdir('tmpDirForTest')

    def close(self):
        self.rmdir('tmpDirForTest')
        self.executor.close(force=True)

    def runCommand(self, cmd):
        """
        Run shell commands on the RemoteServer
        @param cmd: the shell command shall executed on RemoteServer
        """
        if(self._user is None):
            self.executor.sendline('ssh %s \"%s\"' % (self._host, cmd))
            self.wait_server()
            return self.executor.before
        else:
            raise NotImplementedError("Not implemented with user&pswd.")

    def upload(self, srcDir, dstDir='tmpDirForTest'):
        """
        Upload local files or dirs to RemoteServer
        @param srcDir: local file or dir
        @param dstDir: remote dir
        """
        if os.path.exists(srcDir):
            if os.path.isfile(srcDir):
                self.executor.sendline('scp %s %s:tmpDirForTest' % (srcDir, self._host))
                self.wait_server(600)
            elif os.path.isdir(srcDir):
                self.executor.sendline('scp -r %s %s:tmpDirForTest' % (srcDir, self._host))
                self.wait_server(600)
            else:
                raise ValueError("Wrong srcDir type: %s" % srcDir)
            if not self.isDirExists('tmpDirForTest/%s' % srcDir):
                raise RuntimeError("Failed to upload local dir to RemoteServer")
            elif 'tmpDirForTest' != dstDir:
                self.runCommand("sudo cp -r tmpDirForTest/%s %s" % (srcDir, dstDir))
        else:
            raise IOError("srcDir is not exist")

    def download(self, srcDir, dstDir='.'):
        """
        Download files or dirs from RemoteServer
        @param srcDir: remote file or dir
        @param dstDir: local dir
        """
        if not self.isDirExists(srcDir):
            raise IOError("srcDir is not exist")

        self.executor.sendline('scp %s:%s %s' % (self._host, srcDir, dstDir))
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
            raise RuntimeError("ssh config error")
        elif 4 == switch:
            self.executor.sendline('yes')
            self.wait_server(timeout)
        else:
            raise Exception("UnkownError")
#end of class RemoteServer

