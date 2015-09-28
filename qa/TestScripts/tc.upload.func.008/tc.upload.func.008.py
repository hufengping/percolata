#!/usr/bin/env python
#created by Yifei.Fu at 2015-01-22


TESTCASE_ID="Tc.upload.func.008"
TESTCASE_PRI= "M"

import os,sys,pexpect,time


if __name__ == '__main__':
    """Upload module can upload data to new DP server after DP migrated"""
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
    #login to vpn,dp,newdp
    ssh_vpn_proc = pexpect.spawn("ssh %s"%(conf['vpns']['1st']['ssh']))
    wait_server(conf,ssh_vpn_proc,'vpn')
    ssh_dp_proc = pexpect.spawn("ssh %s"%(conf['dps']['1st']['ssh']))
    wait_server(conf,ssh_dp_proc,'dp')
    ssh_newdp_proc = pexpect.spawn("ssh %s"%(conf['dps']['2nd']['ssh']))
    wait_server(conf,ssh_newdp_proc,'dp')
    #if ./TestBench/ not exist on vpn&dp,then create it
    ssh_vpn_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    wait_server(conf,ssh_vpn_proc,'vpn')
    ssh_dp_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    wait_server(conf,ssh_dp_proc,'dp')
    ssh_newdp_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    wait_server(conf,ssh_newdp_proc,'dp')
    #transmit scripts to vpn,dp,newdp
    newbash_proc = pexpect.spawn('bash')
    newbash_proc.sendline('scp -r %s/tovpn/* %s:./TestBench'%(workdir,conf['vpns']['1st']['ssh']))
    wait_server(conf,newbash_proc)
    newbash_proc.sendline('scp -r %s/todp/* %s:./TestBench'%(workdir,conf['dps']['1st']['ssh']))
    wait_server(conf,newbash_proc)
    newbash_proc.sendline('scp -r %s/todp/* %s:./TestBench'%(workdir,conf['dps']['2nd']['ssh']))
    wait_server(conf,newbash_proc)

    #####################<check precondition>########################
    ssh_vpn_proc.sendline("python check_node_health.py '%s'"%(conf['nodes']['1st']['name']))
    wait_server(conf,ssh_vpn_proc,'vpn')
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('precondition failure: %s'%(ssh_vpn_proc.before))
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
        print('precondition failure: %s'%(ssh_dp_proc.before))
        raise Exception('check_module_health failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('module health ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    #####################<Test procedure>########################
    #modify config on new dp server
    import random
    newvalue = random.randint(0,65535) + int(time.time())
    ssh_newdp_proc.sendline("python update_config.py %s \"%s\""%\
            (conf['nodes']['1st']['name'],str({"testvalue":newvalue,"hostname": "https://phone:11222011@%s"%(conf['dps']['2nd']['addr'])})))
    wait_server(conf,ssh_newdp_proc,'dp')
    if not(ssh_newdp_proc.before.find('failure') == -1):
        print('update config failure: %s'%(ssh_newdp_proc.before))
        raise Exception('update config failure')
    elif not(ssh_newdp_proc.before.find('success') == -1):
        print('update config ok.')
    else:
        print('abortion failure: %s'%(ssh_newdp_proc.before))
        raise Exception('abortion failure')

    #migrating DP server
    ssh_dp_proc.sendline("python update_config.py %s \"%s\""%\
            (conf['nodes']['1st']['name'],str({"hostname": "https://phone:11222011@%s"%(conf['dps']['2nd']['addr'])})))
    wait_server(conf,ssh_dp_proc,'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('update config failure: %s'%(ssh_dp_proc.before))
        raise Exception('update config failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('update config ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    time.sleep(120)

    nameString = str(random.randint(0,65535) + int(time.time()))
    #login to node
    ssh_vpn_proc.sendline("ssh -p 443 %s"%(conf['nodes']['1st']['ssh']))
    wait_server(conf,ssh_vpn_proc,'node')

    #stop FusionSensor
    ssh_vpn_proc.sendline("am force-stop com.baysensors.FusionSensor")
    wait_server(conf,ssh_vpn_proc,'node')

    #clear data dir, generate file
    ssh_vpn_proc.sendline("rm %s/*"%(conf['dev_wifi_dir']))
    wait_server(conf,ssh_vpn_proc,'node')
    ssh_vpn_proc.sendline("touch %s"%(os.path.join(conf['dev_wifi_dir'],nameString)))
    wait_server(conf,ssh_vpn_proc,'node')

    #start FusionSensor
    ssh_vpn_proc.sendline("am start -n com.baysensors.FusionSensor/com.baysensors.embedded.os.android.fusionsensor.FusionSensor")
    wait_server(conf,ssh_vpn_proc,'node')

    ssh_vpn_proc.sendline("exit")
    wait_server(conf,ssh_vpn_proc,'vpn')
    time.sleep(120)
    #####################<check postcondition>########################
    ssh_vpn_proc.sendline("python check_config.py '%s' \"%s\""%\
            (conf['nodes']['1st']['name'],str({"testvalue":newvalue})))
    wait_server(conf,ssh_vpn_proc,'vpn')
    if not(ssh_vpn_proc.before.find('failure') == -1):
        print('postcondition failure: %s'%(ssh_vpn_proc.before))
        raise Exception('check_config failure')
    elif not(ssh_vpn_proc.before.find('success') == -1):
        print('check config ok.')
    else:
        print('abortion failure: %s'%(ssh_vpn_proc.before))
        raise Exception('abortion failure')

    ssh_newdp_proc.sendline("python check_module_health.py '%s' \"%s\""%\
            (conf['nodes']['1st']['name'],str(['log','config','upload','sysmon','video'])))
    wait_server(conf,ssh_newdp_proc,'dp')
    if not(ssh_newdp_proc.before.find('failure') == -1):
        print('postcondition failure: %s'%(ssh_newdp_proc.before))
        raise Exception('check_module_health failure')
    elif not(ssh_newdp_proc.before.find('success') == -1):
        print('check module health ok.')
    else:
        print('abortion failure: %s'%(ssh_newdp_proc.before))
        raise Exception('abortion failure')

    ssh_newdp_proc.sendline("python check_file_exist.py %s %s"%(os.path.join(conf['svr_wifi_dir'],conf['nodes']['1st']['name']),nameString))
    wait_server(conf,ssh_newdp_proc,'dp')
    if not(ssh_newdp_proc.before.find('failure') == -1):
        print('postcondition failure: %s'%(ssh_newdp_proc.before))
        raise Exception('check_data_exist failure')
    elif not(ssh_newdp_proc.before.find('success') == -1):
        print('check_data_exist success.')
    else:
        print('abortion failure: %s'%(ssh_newdp_proc.before))
        raise Exception('abortion failure')

    #congratulations:
    print('TestCase finished success')

    #restore
    ssh_dp_proc.sendline("python restore_config.py %s"%(conf['nodes']['1st']['name']))
    wait_server(conf,ssh_dp_proc,'dp')

    ssh_dp_proc.sendline("python update_config.py %s \"%s\""%\
            (conf['nodes']['1st']['name'],str({"hostname": "https://phone:11222011@%s"%(conf['dps']['1st']['addr'])})))
    wait_server(conf,ssh_dp_proc,'dp')
    if not(ssh_dp_proc.before.find('failure') == -1):
        print('update config failure: %s'%(ssh_dp_proc.before))
        raise Exception('update config failure')
    elif not(ssh_dp_proc.before.find('success') == -1):
        print('update config ok.')
    else:
        print('abortion failure: %s'%(ssh_dp_proc.before))
        raise Exception('abortion failure')

    ssh_newdp_proc.sendline("python update_config.py %s \"%s\""%\
            (conf['nodes']['1st']['name'],str({"hostname": "https://phone:11222011@%s"%(conf['dps']['1st']['addr'])})))
    wait_server(conf,ssh_newdp_proc,'dp')
    if not(ssh_newdp_proc.before.find('failure') == -1):
        print('update config failure: %s'%(ssh_newdp_proc.before))
        raise Exception('update config failure')
    elif not(ssh_newdp_proc.before.find('success') == -1):
        print('update config ok.')
    else:
        print('abortion failure: %s'%(ssh_newdp_proc.before))
        raise Exception('abortion failure')

    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
    ssh_newdp_proc.close(force=True)
