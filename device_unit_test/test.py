#!/usr/bin/env python

import pexpect
def timeout_handler(d):
    pass

print("****AUTOMATED TEST BEGIN****")
pexpect.run('python ../test_main.py',events={pexpect.TIMEOUT:timeout_handler})
with open('test_log','r') as log:
    for ln in log:
        if not(ln.find('ERROR') is -1):
            print("="*30)
            print(ln)
            print("-"*30)
            break
timestr = time.strftime("%H_%m-%d-%Y") 
pexpect.run('mv test_log test_log%s'%(timestr),events={pexpect.TIMEOUT:timeout_handler})
