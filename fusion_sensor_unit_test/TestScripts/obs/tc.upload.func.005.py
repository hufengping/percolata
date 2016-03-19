#!/usr/bin/env python
# created by Yifei.Fu at 2015-03-23


TESTCASE_ID = "Tc.upload.func.005"
TESTCASE_PRI = "L"

import os
import sys
import pexpect
import time

if __name__ == '__main__':
    """Upload module can upload wifi files which have correct format."""

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
    print(ssh_vpn_proc.before)
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('precondition failure: %s' % (ssh_vpn_proc.before))
        raise Exception('check_node_health failure')
    elif not(ssh_vpn_proc.before.find('success') == -1):
        print('node health ok.')
    else:
        print('abortion failure.')
        print(ssh_vpn_proc.before)
        raise Exception('abortion failure')
    # 2nd para for check_module_health: 'config','log'
    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\"" %
                         (conf['nodes']['1st']['name'], str(['config', 'log'])))
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
    import random
    nameString = str(random.randint(0, 65535) + int(time.time()))
    # login to node
    ssh_vpn_proc.sendline("ssh -p 443 %s" % (conf['nodes']['1st']['ssh']))
    wait_server(conf, ssh_vpn_proc, 'node')

    # stop FusionSensor
    ssh_vpn_proc.sendline("am force-stop com.baysensors.FusionSensor")
    wait_server(conf, ssh_vpn_proc, 'node')

    # clear data dir, generate file
    ssh_vpn_proc.sendline("rm %s/*" % (conf['dev_video_dir']))
    wait_server(conf, ssh_vpn_proc, 'node')

    # what's the upper size limit of video files
    timeStr = time.strftime("%Y-%m-%d-%H-%M-%S",time.gmtime())
    ssh_vpn_proc.sendline(
        "busybox dd if=/dev/zero bs=1M count=8 of=%s" %
        (os.path.join(
            conf['dev_video_dir'],
            "es-%s_1_%s.3gp" % (timeStr, nameString))))
    wait_server(conf, ssh_vpn_proc, 'node')

    # start FusionSensor
    ssh_vpn_proc.sendline(
        "am start -n com.baysensors.FusionSensor/com.baysensors.embedded.os.android.fusionsensor.FusionSensor")
    wait_server(conf, ssh_vpn_proc, 'node')

    ssh_vpn_proc.sendline("exit")
    wait_server(conf, ssh_vpn_proc, 'vpn')

    #####################<check postcondition>########################
    counter = 30
    while(counter > 0):
        ssh_dp_proc.sendline(
            "python check_file_exist.py %s %s" %
            (os.path.join(
                conf['svr_video_dir'],
                conf['nodes']['1st']['name']),
                nameString))
        wait_server(conf, ssh_dp_proc, 'dp')
        if not(ssh_dp_proc.before.find('success') == -1):
            print('check_data_exist success.')
            break
        else:
            counter -= 1
            print('try %s times.' % (str(30 - counter)))
            time.sleep(120)
    if(0 == counter):
        print('postcondition failure: %s' % (ssh_dp_proc.before))
        raise Exception('check_data_exist failure')

    ssh_vpn_proc.sendline("python check_node_health.py '%s'" % (conf['nodes']['1st']['name']))
    wait_server(conf, ssh_vpn_proc, 'vpn')
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('postcondition failure: %s' % (ssh_vpn_proc.before))
        raise Exception('check_node_health failure')
    elif not(ssh_vpn_proc.before.find('success') == -1):
        print('node health ok.')
    else:
        print('abortion failure.')
        print(ssh_vpn_proc.before)
        raise Exception('abortion failure')

    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\"" %
                         (conf['nodes']['1st']['name'], str(['log', 'config', 'upload', 'sysmon', 'video'])))
    wait_server(conf, ssh_dp_proc, 'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('postcondition failure: %s' % (ssh_dp_proc.before))
        raise Exception('check_module_health failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure.')
        print(ssh_dp_proc.before)
        raise Exception('abortion failure')

    ssh_dp_proc.sendline("python check_log.py '%s'" % (conf['nodes']['1st']['name']))
    wait_server(conf, ssh_dp_proc, 'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('postcondition failure: %s' % (ssh_dp_proc.before))
        raise Exception('check_log failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure.')
        print(ssh_dp_proc.before)
        raise Exception('abortion failure')

    # congratulations:
    print('TestCase finished success')

    # restore
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
