#!/usr/bin/env python
# created by Yifei.Fu at 2015-03-25


TESTCASE_ID = "Tc.upload.func.010"
TESTCASE_PRI = "M"

import os
import sys
import pexpect

if __name__ == '__main__':
    DESCSTR="""When upload module detect that video worker havent generate data file for a while,and which is unexpected,It will add a event log."""

    #####################<prerequisites>########################
    # caller pass the WORKDIR pathname,test CONF by commandline args
    WORKDIR = sys.argv[1]
    CONF = eval(sys.argv[2])
    os.chdir(WORKDIR)

    # load TestModules
    sys.path.append(CONF["test_lib_dir"])
    import interact

    # prepare files for vpn dp
    interact.prepare_file(CONF, 'vpn')
    interact.prepare_file(CONF, 'dp')

    # login to vpn,dp
    ssh_vpn_proc = pexpect.spawn("ssh %s" % (CONF['vpns']['1st']['ssh']))
    interact.wait_server(CONF, ssh_vpn_proc, 'vpn')
    ssh_dp_proc = pexpect.spawn("ssh %s" % (CONF['dps']['1st']['ssh']))
    interact.wait_server(CONF, ssh_dp_proc, 'dp')
    # if ./TestBench/ not exist on vpn&dp,then create it
    ssh_vpn_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    interact.wait_server(CONF, ssh_vpn_proc, 'vpn')
    ssh_dp_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
    interact.wait_server(CONF, ssh_dp_proc, 'dp')
    # transmit scripts to vpn,dp
    newbash_proc = pexpect.spawn('bash')
    newbash_proc.sendline(
        'scp -r %s/tovpn/* %s:./TestBench' %
        (WORKDIR, CONF['vpns']['1st']['ssh']))
    interact.wait_server(CONF, newbash_proc)
    newbash_proc.sendline('scp -r %s/todp/* %s:./TestBench' % (WORKDIR, CONF['dps']['1st']['ssh']))
    interact.wait_server(CONF, newbash_proc)

    #####################<check precondition>########################

    #####################<Test procedure>########################
    # TODO this functionality haven't been realized yet
    print('abortion failure.')
    print(ssh_dp_proc.before)
    raise Exception('abortion failure')
    #####################<check postcondition>########################

    # congratulations:
    print('TestCase finished success')

    # restore
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
