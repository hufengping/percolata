#!/usr/bin/env python
# created by Yifei.Fu at 2015-03-27


TESTCASE_ID = "Tc.vworker.func.003"
TESTCASE_PRI = "M"

import os
import sys
import pexpect
import time


if __name__ == '__main__':
    """Under video mode, video worker can record relative data and put the data into specified dir"""

    #####################<prerequisites>########################
    # caller pass the workdir pathname,test conf by commandline args
    workdir = sys.argv[1]
    conf = eval(sys.argv[2])
    os.chdir(workdir)

    # load TestModules
    sys.path.append(conf["test_lib_dir"])
    import interact

    # prepare files for vpn dp
    interact.prepare_file(conf, 'vpn')
    interact.prepare_file(conf, 'dp')

    # login to vpn,dp
    ssh_vpn_proc = pexpect.spawn("ssh %s" % (conf['vpns']['1st']['ssh']))
    interact.wait_server(conf, ssh_vpn_proc, 'vpn')
    ssh_dp_proc = pexpect.spawn("ssh %s" % (conf['dps']['1st']['ssh']))
    interact.wait_server(conf, ssh_dp_proc, 'dp')
    # if ./TestBench/ not exist on vpn&dp,then create it
    ssh_vpn_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    interact.wait_server(conf, ssh_vpn_proc, 'vpn')
    ssh_dp_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    interact.wait_server(conf, ssh_dp_proc, 'dp')
    # transmit scripts to vpn,dp
    newbash_proc = pexpect.spawn('bash')
    newbash_proc.sendline(
        'scp -r %s/tovpn/* %s:./TestBench' %
        (workdir, conf['vpns']['1st']['ssh']))
    interact.wait_server(conf, newbash_proc)
    newbash_proc.sendline('scp -r %s/todp/* %s:./TestBench' % (workdir, conf['dps']['1st']['ssh']))
    interact.wait_server(conf, newbash_proc)

    #####################<check precondition>########################
    ssh_vpn_proc.sendline("python check_node_health.py '%s'" % (conf['nodes']['1st']['name']))
    interact.wait_server(conf, ssh_vpn_proc, 'vpn')
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
    interact.wait_server(conf, ssh_dp_proc, 'dp')
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
    #####set to video mode, check that relative data can be upload successfully
    interact.set_vworker_mode(conf,
                              ssh_dp_proc,
                              '1st',
                              'video'
                             )
    interact.chk_vworker_mode(conf,
                              ssh_dp_proc,
                              '1st',
                              'video'
                             )

    #####################<check postcondition>########################
    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\"" %
                         (conf['nodes']['1st']['name'], str(['log', 'config', 'upload', 'sysmon', 'video'])))
    interact.wait_server(conf, ssh_dp_proc, 'dp')
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
    interact.wait_server(conf, ssh_dp_proc, 'dp')
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
