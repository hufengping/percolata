#!/usr/bin/env python
# created by Yifei.Fu at 2015-02-10


TESTCASE_ID = "Tc.config.reli.003"
TESTCASE_PRI = "L"

import os
import sys
import pexpect
import time

if __name__ == '__main__':
    """Config module need to check remote config file \
            after DP server update it with wrong file status"""

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
                         (conf['nodes']['1st']['name'], str(['log', 'config'])))
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
    newvalue = random.randint(0, 65535) + int(time.time())
    ssh_dp_proc.sendline("python update_config.py %s \"%s\"" %
                         (conf['nodes']['1st']['name'], str({"testvalue": newvalue})))
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
    # modify server-end config file with wrong status
    ssh_dp_proc.sendline("chmod 400 %s.json" %
                         (os.path.join(conf['svr_conf_dir'], conf['nodes']['1st']['name'])))
    wait_server(conf, ssh_dp_proc, 'dp')
    ssh_dp_proc.sendline("touch %s.json.swp" %
                         (os.path.join(conf['svr_conf_dir'], '.' + conf['nodes']['1st']['name'])))
    wait_server(conf, ssh_dp_proc, 'dp')

    time.sleep(180)

    #####################<check postcondition>########################
    ssh_vpn_proc.sendline("python check_config.py '%s' \"%s\"" %
                          (conf['nodes']['1st']['name'], str({"testvalue": newvalue})))
    wait_server(conf, ssh_vpn_proc, 'vpn')
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('postcondition failure: %s' % (ssh_vpn_proc.before))
        raise Exception('check config failure')
    elif not(ssh_vpn_proc.before.find('success') == -1):
        print('check config ok.')
    else:
        print('abortion failure.')
        print(ssh_vpn_proc.before)
        raise Exception('abortion failure')

    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\"" %
                         (conf['nodes']['1st']['name'], str(['log', 'config'])))
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
    ssh_dp_proc.sendline("chmod 644 %s.json" %
                         (os.path.join(conf['svr_conf_dir'], conf['nodes']['1st']['name'])))
    wait_server(conf, ssh_dp_proc, 'dp')
    ssh_dp_proc.sendline("rm -f %s.json.swp" %
                         (os.path.join(conf['svr_conf_dir'], '.' + conf['nodes']['1st']['name'])))
    wait_server(conf, ssh_dp_proc, 'dp')
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
