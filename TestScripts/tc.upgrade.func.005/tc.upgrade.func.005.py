#!/usr/bin/env python
#created by Yifei.Fu at 2015-04-12


TESTCASE_ID="Tc.upgrade.func.005"
TESTCASE_PRI= "M"

import os,sys,pexpect,time

if __name__ == '__main__':
    """Data file should not be removed when nodes are upgraded."""

    #####################<prerequisites>########################
    #caller pass the workdir pathname,test conf by commandline args
    workdir = sys.argv[1]
    conf = eval(sys.argv[2])
    os.chdir(workdir)

    #load TestModules
    sys.path.append(conf["test_lib_dir"])
    from interact import *

    #prepare files for vpn dp
    prepare_file(conf,'vpn')
    prepare_file(conf,'dp')

    #login to vpn,dp
    ssh_vpn_proc = pexpect.spawn("ssh %s"%(conf['vpns']['1st']['ssh']))
    wait_server(conf,ssh_vpn_proc,'vpn')
    ssh_dp_proc = pexpect.spawn("ssh %s"%(conf['dps']['1st']['ssh']))
    wait_server(conf,ssh_dp_proc,'dp')
    #if ./TestBench/ not exist on vpn&dp,then create it
    ssh_vpn_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    wait_server(conf,ssh_vpn_proc,'vpn')
    ssh_dp_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    wait_server(conf,ssh_dp_proc,'dp')
    #transmit scripts to vpn,dp
    newbash_proc = pexpect.spawn('bash')
    newbash_proc.sendline('scp -r %s/tovpn/* %s:./TestBench'%(workdir,conf['vpns']['1st']['ssh']))
    wait_server(conf,newbash_proc)
    newbash_proc.sendline('scp -r %s/todp/* %s:./TestBench'%(workdir,conf['dps']['1st']['ssh']))
    wait_server(conf,newbash_proc)

    #####################<check precondition>########################
    ssh_vpn_proc.sendline("python check_node_health.py '%s'"%(conf['nodes']['1st']['name']))
    wait_server(conf,ssh_vpn_proc,'vpn')
    print(ssh_vpn_proc.before)
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('precondition failure: %s'%(ssh_vpn_proc.before))
        raise Exception('check_node_health failure')
    elif not(ssh_vpn_proc.before.find('success') == -1):
        print('node health ok.')
    else:
        print('abortion failure: %s'%(ssh_vpn_proc.before))
        raise Exception('abortion failure')
    #2nd para for check_module_health: 'config','log'
    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\""%\
            (conf['nodes']['1st']['name'],str(['config','log','upgrade'])))
    wait_server(conf,ssh_dp_proc,'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('precondition failure: %s'%(ssh_dp_proc.before))
        raise Exception('check_module_health failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    #####################<Test procedure>########################
    ssh_dp_proc.sendline("python update_config.py %s \"%s\""%\
            (conf['nodes']['1st']['name'],str({"FusionAdmin":{"softwareUpdate":{"enable":"yes","forceUpdate":"true"}}})))
    wait_server(conf,ssh_dp_proc,'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('update config failure: %s'%(ssh_dp_proc.before))
        raise Exception('update config failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('update config ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    occurTime = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime())
    timeStr1 = time.strftime("%m-%d-%Y",time.gmtime())
    timeStr2 = time.strftime("%Y%m%d%H%M",time.gmtime())
    ssh_dp_proc.sendline("python update_config.py %s \"%s\""%\
            ('updateAdminConfig',str({"FusionSensor":{"version":{"%s.v1.0.%s-test-H535"%(timeStr1,timeStr2)}}})))
    wait_server(conf,ssh_dp_proc,'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('update config failure: %s'%(ssh_dp_proc.before))
        raise Exception('update config failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('update config ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    time.sleep(300)
    ssh_dp_proc.sendline("cat /log/placement_%s.txt |grep 'updated FusionSensor'|tail -1"%\
            (conf['nodes']['1st']['name']))
    wait_server(conf,ssh_dp_proc,'dp')
    recvTime = ssh_dp_proc.before.split('\r\n')[-2].split('|')[1]
    if (recvTime < occurTime):
        print('check log failure: %s'%(ssh_dp_proc.before))
        raise Exception('check_log failure')
    #####################<check postcondition>########################
    #TODO check if data files has been removed .

    ssh_vpn_proc.sendline("python check_node_health.py '%s'"%(conf['nodes']['1st']['name']))
    wait_server(conf,ssh_vpn_proc,'vpn')
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('postcondition failure: %s'%(ssh_vpn_proc.before))
        raise Exception('check_node_health failure')
    elif not(ssh_vpn_proc.before.find('success') == -1):
        print('node health ok.')
    else:
        print('abortion failure: %s'%(ssh_vpn_proc.before))
        raise Exception('abortion failure')

    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\""%\
            (conf['nodes']['1st']['name'],str(['log','config','upload','upgrade','video'])))
    wait_server(conf,ssh_dp_proc,'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('postcondition failure: %s'%(ssh_dp_proc.before))
        raise Exception('check_module_health failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    ssh_dp_proc.sendline("python check_log.py '%s'"%(conf['nodes']['1st']['name']))
    wait_server(conf,ssh_dp_proc,'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('postcondition failure: %s'%(ssh_dp_proc.before))
        raise Exception('check_log failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    #congratulations:
    print('TestCase finished success')


    #restore
    ssh_dp_proc.sendline("python restore_config.py")
    wait_server(conf,ssh_dp_proc,'dp')
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)

