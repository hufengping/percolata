__author__ = 'fengpinghu'
#coding=utf-8
import os,sys
from pexpect import *
print 'run("ls") have not log!'
run("ls")
print 'logfile = run("ls") : log is in logfile!'
log = run("ls")
print log,
print 'run("ls",logfile=sys.stdout): log standard output'
run("ls",logfile=sys.stdout)

(command_output, exitstatus) = run ('ls -l /bin', withexitstatus=1)  #capture exit status
run ('scp foo myname@host.example.com:.', events={'(?i)password': '123456'}) #很实用
