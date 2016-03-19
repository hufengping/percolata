#!/usr/bin/env python
# created by Yifei.Fu at 2015-02-11


TESTCASE_ID = "Tc.config.reli.005"
TESTCASE_PRI = "M"

import os
import sys
import pexpect
import time

if __name__ == '__main__':
    """Config module need to check local config
    file for wrong config format after start up."""

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
    # modify server-end config, wait 2 min for device updating.
    #    then modify device-end config, we expect that after FS startup,
    #    it will check its local config, while founding defect, it would
    #    somehow restore the local config
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

    time.sleep(120)

    ssh_vpn_proc.sendline("ssh -p 443 %s" % (conf['nodes']['1st']['ssh']))
    wait_server(conf, ssh_vpn_proc, 'node')
    ssh_vpn_proc.sendline("cd %s" % (conf['dev_conf_dir']))
    wait_server(conf, ssh_vpn_proc, 'node')
    ssh_vpn_proc.sendline("cp fusion-sensor.json bak.%s" % (newvalue))
    wait_server(conf, ssh_vpn_proc, 'node')
    ssh_vpn_proc.sendline("echo 'error format test' > %s" %
                          (os.path.join(conf['dev_conf_dir'], 'fusion-sensor.json')))
    wait_server(conf, ssh_vpn_proc, 'node')
    # stop FusionSensor
    ssh_vpn_proc.sendline("am force-stop com.baysensors.FusionSensor")
    wait_server(conf, ssh_vpn_proc, 'node')

    # start FusionSensor
    ssh_vpn_proc.sendline(
        "am start -n com.baysensors.FusionSensor/com.baysensors.embedded.os.android.fusionsensor.FusionSensor")
    wait_server(conf, ssh_vpn_proc, 'node')

    time.sleep(120)

    ssh_vpn_proc.sendline("exit")
    wait_server(conf, ssh_vpn_proc, 'vpn')
    #####################<check postcondition>########################
    ssh_vpn_proc.sendline("python check_config.py '%s' \"%s\"" %
                          (conf['nodes']['1st']['name'], str({"testvalue": newvalue})))
    wait_server(conf, ssh_vpn_proc, 'vpn')
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('postcondition failure: %s' % (ssh_vpn_proc.before))
    elif not(ssh_vpn_proc.before.find('success') == -1):
        print('node health ok.')
    else:
        print('abortion failure.')
        print(ssh_vpn_proc.before)

    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\"" %
                         (conf['nodes']['1st']['name'], str(['log', 'config'])))
    wait_server(conf, ssh_dp_proc, 'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('postcondition failure: %s' % (ssh_dp_proc))
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure.')
        print(ssh_dp_proc.before)

    # congratulations:
    print('TestCase finished success')

    # restore
    ssh_vpn_proc.sendline("ssh -p 443 %s" % (conf['nodes']['1st']['ssh']))
    wait_server(conf, ssh_vpn_proc, 'node')
    ssh_vpn_proc.sendline("cd %s" % (conf['dev_conf_dir']))
    wait_server(conf, ssh_vpn_proc, 'node')
    ssh_vpn_proc.sendline("mv -f bak.%s %s" %
                          (newvalue, 'fusion-sensor.json'))
    wait_server(conf, ssh_vpn_proc, 'node')
    ssh_dp_proc.sendline("python restore_config.py %s" % (conf['nodes']['1st']['name']))
    wait_server(conf, ssh_dp_proc, 'dp')
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
