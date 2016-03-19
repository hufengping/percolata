#!/usr/bin/env python

import os
import sys
import pexpect
import re

if __name__ == '__main__':
    """
        used to modify scripts in batch, TO BE CAREFUL!
    """
    # filter used for finding scripts
    regex1 = re.compile(r'tc\.(?P<module>\w*)\.(?P<testType>\w*)\.(?P<testId>\d*)')
    # filter used for determining context, change this as needed
    regex2 = re.compile(r'ssh_(?P<serverType>\w*)_proc.before')
    # filter used for locating targets, change this as needed
    #regex3 = re.compile(r"print\('abortion failure\.'\)")
    #regex3 = re.compile(r"conf\['svr_(?:video|wifi|blob)_dir'\]")
    regex3 = re.compile(r"(?P<prefix>\s*)print\('abortion.*?(?P<mid>\(.*\.before\))\)")
    global context
    for dir in os.walk(os.getcwd() + os.sep + 'TestScripts' + os.sep):
        m1 = regex1.search(dir[0])
        if not(m1 is None):
            scriptName = dir[0] + os.sep + m1.group() + r".py"
            if (os.path.isfile(scriptName)):
                script = open(scriptName, 'r')
                inlist = script.readlines()
                script.close()
                outlist = []
                for ln in inlist:
#                    m2 = regex2.search(ln)
#                    if not (None == m2):
#                        context = m2.group()
#                        outlist.append(ln)
#                        continue
                    m3 = regex3.match(ln)
                    if not(None == m3):
                        outlist.append(m3.group(1) + "print('abortion failure.')" + "\n")
                        outlist.append(m3.group(1) + "print"+m3.group(2) + "\n")
#                        ln = ln.replace(m3.group(), r"os.path.join(%s,%s)" %
#                                        (m3.group(), "conf['nodes']['1st']['name']"))
                    else:
                        outlist.append(ln)
                script = open(scriptName, 'w')
                script.writelines(outlist)
                script.flush()
                script.close()
