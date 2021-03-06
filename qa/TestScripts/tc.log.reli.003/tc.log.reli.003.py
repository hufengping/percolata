#!/usr/bin/env python
#created by Yifei.Fu at 2015-02-26


TESTCASE_ID="Tc.log.reli.003"
TESTCASE_PRI= "L"

import os,sys,pexpect,time

if __name__ == '__main__':
    """When log module failed to write local log file, it can keep the logs somehow."""

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
    ssh_dp_proc.sendline("python check_module_health.py '%s' \"%s\""%(conf['nodes']['1st']['name'],str(['log'])))
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
    #umount /storage/emulated/legacy to make writing log failure
    ssh_vpn_proc.sendline("ssh -p 443 %s"%(conf['nodes']['1st']['ssh']))
    wait_server(conf,ssh_vpn_proc,'node')
    ssh_vpn_proc.sendline("busybox umount /storage/emulated/legacy")
    wait_server(conf,ssh_vpn_proc,'node')
    ssh_vpn_proc.sendline("exit")
    wait_server(conf,ssh_vpn_proc,'vpn')
    #record event time
    occurTime = time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime())
    # stop wlan0 on device for a specified duration(i.e. 5s)
    ssh_vpn_proc_stop_wlan = pexpect.spawn("ssh %s"%(conf['vpns']['1st']['ssh']))
    wait_server(conf,ssh_vpn_proc_stop_wlan,'vpn')
    ssh_vpn_proc_stop_wlan.sendline("cd TestBench")
    wait_server(conf,ssh_vpn_proc_stop_wlan,'vpn')
    ssh_vpn_proc_stop_wlan.sendline("scp -P 443 stopWlan0.sh %s:/mnt/sdcard/"%(conf['nodes']['1st']['ssh']))
    wait_server(conf,ssh_vpn_proc_stop_wlan,'vpn')
    ssh_vpn_proc_stop_wlan.sendline("ssh -p 443 %s"%(conf['nodes']['1st']['ssh']))
    wait_server(conf,ssh_vpn_proc_stop_wlan,'node')
    ssh_vpn_proc_stop_wlan.sendline("cd /mnt/sdcard/;sh stopWlan0.sh 5&")

    #wait for writing log failure
    time.sleep(60)
    #remount /sdcard, we expect that logs would not be lost
    ssh_vpn_proc.sendline("ssh -p 443 %s"%(conf['nodes']['1st']['ssh']))
    wait_server(conf,ssh_vpn_proc,'node')
    ssh_vpn_proc.sendline("busybox mount /mnt/shell/emulated/0 /storage/emulated/legacy")
    wait_server(conf,ssh_vpn_proc,'node')
    ssh_vpn_proc.sendline("exit")
    wait_server(conf,ssh_vpn_proc,'vpn')
    #wait for upload logs
    time.sleep(300)

    #####################<check postcondition>########################
    ssh_dp_proc.sendline("cat /log/placement_%s.txt |grep FS-wificontrol|tail -1"%\
            (conf['nodes']['1st']['name']))
    wait_server(conf,ssh_dp_proc,'dp')
    recvTime = ssh_dp_proc.before.split('\r\n')[-2].split('|')[1]
    if (recvTime < occurTime):
        print('check log failure: %s'%(ssh_dp_proc.before))
        raise Exception('check_log failure')

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
            (conf['nodes']['1st']['name'],str(['log','config'])))
    wait_server(conf,ssh_dp_proc,'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('postcondition failure: %s'%(ssh_dp_proc.before))
        raise Exception('check_module_health failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    #congratulations:
    print('TestCase finished success')


    #restore
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
    ssh_vpn_proc_stop_wlan.close(force=True)
