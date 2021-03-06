#!/usr/bin/env python
# created by Yifei.Fu at 2015-03-27


TESTCASE_ID = "Tc.vworker.func.002"
TESTCASE_PRI = "M"

import os
import sys
import pexpect
import time


if __name__ == '__main__':
    """Under installation mode, video worker can record relative data and put the data into specified dir"""

    #####################<prerequisites>########################
    # caller pass the workdir pathname,test conf by commandline args
    workdir = sys.argv[1]
    conf = eval(sys.argv[2])
    os.chdir(workdir)

    # load TestModules
    sys.path.append(conf["test_lib_dir"])
    from interact import *

    # prepare files for vpn dp
    prepare_file(conf, 'vpn')
    prepare_file(conf, 'dp')

    # login to vpn,dp
    ssh_vpn_proc = pexpect.spawn("ssh %s" % (conf['vpns']['1st']['ssh']))
    wait_server(conf, ssh_vpn_proc, 'vpn')
    ssh_dp_proc = pexpect.spawn("ssh %s" % (conf['dps']['1st']['ssh']))
    wait_server(conf, ssh_dp_proc, 'dp')
    # if ./TestBench/ not exist on vpn&dp,then create it
    ssh_vpn_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    wait_server(conf, ssh_vpn_proc, 'vpn')
    ssh_dp_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    wait_server(conf, ssh_dp_proc, 'dp')
    # transmit scripts to vpn,dp
    newbash_proc = pexpect.spawn('bash')
    newbash_proc.sendline(
        'scp -r %s/tovpn/* %s:./TestBench' %
        (workdir, conf['vpns']['1st']['ssh']))
    wait_server(conf, newbash_proc)
    newbash_proc.sendline('scp -r %s/todp/* %s:./TestBench' % (workdir, conf['dps']['1st']['ssh']))
    wait_server(conf, newbash_proc)

    #####################<check precondition>########################
    ssh_vpn_proc.sendline("python check_node_health.py '%s'" % (conf['nodes']['1st']['name']))
    wait_server(conf, ssh_vpn_proc, 'vpn')
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('precondition failure: %s' % (ssh_vpn_proc.before))
        raise Exception('check_node_health failure')
    elif not(ssh_vpn_proc.before.find('success') == -1):
        print('node health ok.')
    else:
        print('abortion failure.')
        print(ssh_vpn_proc.before)
        raise Exception('abortion failure')

    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\"" %
                         (conf['nodes']['1st']['name'], str(['log', 'config', 'video'])))
    wait_server(conf, ssh_dp_proc, 'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('precondition failure: %s' % (ssh_dp_proc.before))
        raise Exception('check_module_health failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure.')
        print(ssh_dp_proc.before)
        raise Exception('abortion failure')

    #####################<Test procedure>########################
    ssh_dp_proc.sendline("python update_config.py %s \"%s\"" %
                         (conf['nodes']['1st']['name'], str({"installation-mode": "yes"})))
    wait_server(conf, ssh_dp_proc, 'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('update config failure: %s' % (ssh_dp_proc.before))
        raise Exception('update config failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('update config ok.')
    else:
        print('abortion failure.')
        print(ssh_dp_proc.before)
        raise Exception('abortion failure')

    curTime = time.time()
    # consult get_file_num.py
    ssh_dp_proc.sendline("python get_file_num.py %s %s %s" %
                         (os.path.join(conf['svr_video_dir'], conf['nodes']['1st']['name']),
                          'install', curTime))
    wait_server(conf, ssh_dp_proc, 'dp')
    if(ssh_dp_proc.before.find('##number##') == -1):
        print('get_file_num failure: %s' % (ssh_dp_proc.before))
        raise Exception('get_file_num failure')
    tmpList = ssh_dp_proc.before.split('##')
    num1 = int(tmpList[tmpList.index('number') + 1])

    time.sleep(90)
    # T_restart FS. login to node, restart FS to take config into effect immediately
    ssh_vpn_proc.sendline("ssh -p 443 %s" % (conf['nodes']['1st']['ssh']))
    wait_server(conf, ssh_vpn_proc, 'node')

    # stop FusionSensor
    ssh_vpn_proc.sendline("am force-stop com.baysensors.FusionSensor")
    wait_server(conf, ssh_vpn_proc, 'node')

    # start FusionSensor
    ssh_vpn_proc.sendline(
        "am start -n com.baysensors.FusionSensor/com.baysensors.embedded.os.android.fusionsensor.FusionSensor")
    wait_server(conf, ssh_vpn_proc, 'node')

    ssh_vpn_proc.sendline("exit")
    wait_server(conf, ssh_vpn_proc, 'vpn')
    time.sleep(90)

    ssh_dp_proc.sendline("python get_file_num.py %s %s %s" %
                         (os.path.join(conf['svr_video_dir'], conf['nodes']['1st']['name']),
                          'install', curTime))
    wait_server(conf, ssh_dp_proc, 'dp')
    if(ssh_dp_proc.before.find('##number##') == -1):
        print('get_file_num failure: %s' % s(ssh_dp_proc.before))
        raise Exception('get_file_num failure')
    tmpList = ssh_dp_proc.before.split('##')
    num2 = int(tmpList[tmpList.index('number') + 1])

    #####################<check postcondition>########################
    if (num1 >= num2):
        print('TestCase failure')
        raise Exception('TestCase failure')

    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\"" %
                         (conf['nodes']['1st']['name'], str(['log', 'config', 'upload', 'sysmon', 'video'])))
    wait_server(conf, ssh_dp_proc, 'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('postcondition failure: %s' % (ssh_dp_proc))
        raise Exception('check_module_health failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure.')
        print(ssh_dp_proc.before)
        raise Exception('abortion failure')

    # congratulations:
    print('TestCase finished success')

    # restore
    ssh_dp_proc.sendline("python restore_config.py %s" % (conf['nodes']['1st']['name']))
    wait_server(conf, ssh_dp_proc, 'dp')
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
