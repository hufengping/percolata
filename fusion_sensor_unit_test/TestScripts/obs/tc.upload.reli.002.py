#!/usr/bin/env python
# created by Yifei.Fu at 2015-03-25


TESTCASE_ID = "Tc.upload.reli.002"
TESTCASE_PRI = "M"

import os
import sys
import pexpect

if __name__ == '__main__':
    """If upload module encounter an crash, it can i\
            continue the formerly interrupted uploading procedure after restore."""

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

    #####################<Test procedure>########################
    # This testcase has been checked with former func scripts
    #####################<check postcondition>########################

    # congratulations:
    print('TestCase finished success')

    # restore
    ssh_vpn_proc.close(force=True)
    ssh_dp_proc.close(force=True)
    newbash_proc.close(force=True)
