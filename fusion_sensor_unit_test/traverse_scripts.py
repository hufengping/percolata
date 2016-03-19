#!/usr/bin/env python
"""used for statistic quality info of each script"""
import os
import re
import pexpect

if __name__ == '__main__':
    # filter used for finding scripts
    REGEX1 = re.compile(r'tc\.(?P<module>\w*)\.(?P<testType>\w*)\.(?P<testId>\d*)')
    # filter used for determining context, change this as needed
    # REGEX2 = re.compile(r'ssh_(?P<serverType>\w*)_proc.before')
    # filter used for locating targets, change this as needed
    # REGEX3 = re.compile(r"print\('abortion failure\.'\)")
    # REGEX3 = re.compile(r"conf\['svr_(?:video|wifi|blob)_dir'\]")

    for pos in os.walk(os.getcwd() + os.sep + 'TestScripts' + os.sep):
        m1 = REGEX1.search(pos[0])
        if not(m1 is None):
            scriptName = pos[0] + os.sep + m1.group() + r".py"
            if os.path.isfile(scriptName):
                pexpect.run("bash -c \"autopep8 %s\"" %
                            "--in-place --indent-size 4 --max-line-length 100 --aggressive %s" %
                            scriptName
                           )
                pexpect.run("bash -c \"echo 'stat of %s' >> pylint_log\"" %
                            scriptName
                           )
                pexpect.run("bash -c \"pylint %s\"" %
                            "--rcfile /home/jolyon/.pylintrc %s" %
                            "%s | tail -3 >> pylint_log" %
                            scriptName
                           )
