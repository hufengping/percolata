#!/usr/bin/env python
#created by Yifei.Fu at 2015-01-21

import time,os,sys,pexpect,inspect

#timeout toleration:
timeout_count = 3
#eof toleration:
eof_count = 1

def timeout_handler(d = {'event_count':None}):
    c = inspect.currentframe(2)
    if not(None == d['event_count']):
        print(('event_count:'+d['event_count']))
    global timeout_count
    if(0 == timeout_count):
        print('timeout & failure:%s.in file:%s at line:%s'%(time.strftime("%H:%M:%S_%m-%d-%Y" ),c.f_code.co_filename, c.f_lineno))
        time.sleep(0.1)
        raise Exception('TIMEOUT')
    else:
        timeout_count -= 1
#end of timeout_handler

def eof_handler():
    c = inspect.currentframe(2)
    global eof_count
    print eof_count
    if(0 == eof_count):
        print('eof failure:%s.in file:%s at line:%s'%(time.strftime("%H:%M:%S_%m-%d-%Y" ),c.f_code.co_filename, c.f_lineno))
        time.sleep(0.1)
        raise Exception('Unexpected End')
    else:
        eof_count -= 1
#end of eof_handler

def wait_server(conf,proc,server='local',timeout=60):
    time.sleep(0.1)
    #avoid dead loop
    tcount = 3
    while(True):
        if 'local' == server:
            switch = proc.expect([conf['prompt'], pexpect.EOF, pexpect.TIMEOUT, 'assword:', '\(yes/no\)\?'],timeout)
        elif 'vpn' == server:
            switch = proc.expect([conf['vpns']['prompt'], pexpect.EOF, pexpect.TIMEOUT, 'assword:', '\(yes/no\)\?'],timeout)
        elif 'dp' == server:
            switch = proc.expect([conf['dps']['prompt'], pexpect.EOF, pexpect.TIMEOUT, 'assword:', '\(yes/no\)\?'],timeout)
        elif 'node' == server:
            switch = proc.expect([conf['nodes']['prompt'], pexpect.EOF, pexpect.TIMEOUT, 'assword:', '\(yes/no\)\?'],timeout)
        else:
            raise Exception("TypeError")
        if 0 == switch:
            return
        elif 1 == switch:
            eof_handler()
        elif 2 == switch:
            if not(0 == tcount):
                timeout_handler()
                tcount -= 1
            else:
                print('timeout failure: %s'%(proc.before))
                raise Exception("TIMEOUT")
        elif 3 == switch:
            if not(0 == tcount):
                proc.sendline(conf['nodes']['pswd'])
                tcount -= 1
            else:
                print('login failure')
                raise Exception("PSWDError")
        elif 4 == switch:
            proc.sendline('yes')
#end of wait_server

def prepare_file(conf,tag):
    """prepare files for vpns, dps"""
    c = pexpect.spawn('bash')
    wait_server(conf,c)

    if ('vpn' == tag):
        c.sendline("if [ ! -d 'tovpn'    ];then mkdir tovpn;fi")
        wait_server(conf,c)
        for s in conf['tovpn']:
            c.sendline('cp %s ./tovpn'%(os.path.join(conf['test_lib_dir'],s)))
            wait_server(conf,c)
            if not(c.before.find('cannot') == -1):
                print('prepare_file failure: ',c.before)
                raise Exception(c.before)

    elif('dp' == tag):
        c.sendline("if [ ! -d 'todp'    ];then mkdir todp;fi")
        wait_server(conf,c)
        for s in conf['todp']:
            c.sendline('cp %s ./todp'%(os.path.join(conf['test_lib_dir'],s)))
            wait_server(conf,c)
            if not(c.before.find('cannot') == -1):
                print('prepare_file failure: ',c.before)
                raise Exception(c.before)
    else:
        print('failure: unknown server: %s'%(tag))
        raise Exception('unknown server:',tag)
#end of prepare_file

def get_time_region(cur_time):
    """for given cur_time, return cur_region which include cur_time,\
            return opp_region which not include cur_time"""
    cur_region_l = time.gmtime(cur_time + 22*3600)
    cur_region_r = time.gmtime(cur_time + 2*3600)
    opp_region_l = time.gmtime(cur_time + 10*3600)
    opp_region_r = time.gmtime(cur_time + 14*3600)

    return "%s-%s"%(time.strftime('%H:%M',cur_region_l),time.strftime('%H:%M',cur_region_r)),\
        "%s-%s"%(time.strftime('%H:%M',opp_region_l),time.strftime('%H:%M',opp_region_r))
#end of get_time_region

def get_vpn_no(conf):
    import pexpect
    c = pexpect.spawn('bash')
    c.expect('\$')
    vpns = conf['vpns']
    for k in vpns:
        if (k=='prompt')|(k=='pswd'):
            continue
        if not(c.before.find(vpns[k]['name']) == -1):
            return k

    return None
#end of get_vpn_no

def get_dp_no(conf):
    import pexpect
    c = pexpect.spawn('bash')
    c.expect('\$')
    dps = conf['dps']
    for k in dps:
        if (k=='prompt')|(k=='pswd'):
            continue
        if not(c.before.find(dps[k]['name']) == -1):
            return k

    return None
#end of get_dp_no
