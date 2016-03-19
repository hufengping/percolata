#!/usr/bin/env python
# created by Yifei.Fu at 2015-01-21

import time
import os
import sys
import pexpect
import inspect

# timeout toleration:
timeout_count = 3
# eof toleration:
eof_count = 1


def timeout_handler(d={'event_count': None}):
    c = inspect.currentframe(2)
    if not(None == d['event_count']):
        print(('event_count:' + d['event_count']))
    global timeout_count
    if(0 == timeout_count):
        print(
            'timeout & failure:%s.in file:%s at line:%s' %
            (time.strftime("%H:%M:%S_%m-%d-%Y"),
             c.f_code.co_filename,
             c.f_lineno))
        time.sleep(0.1)
        raise Exception('TIMEOUT')
    else:
        timeout_count -= 1
# end of timeout_handler


def eof_handler():
    c = inspect.currentframe(2)
    global eof_count
    print eof_count
    if(0 == eof_count):
        print(
            'eof failure:%s.in file:%s at line:%s' %
            (time.strftime("%H:%M:%S_%m-%d-%Y"),
             c.f_code.co_filename,
             c.f_lineno))
        time.sleep(0.1)
        raise Exception('Unexpected End')
    else:
        eof_count -= 1
# end of eof_handler


def wait_server(conf, proc, server='local', timeout=60):
    time.sleep(0.1)
    # avoid dead loop
    tcount = 3
    while(True):
        if 'local' == server:
            switch = proc.expect([conf['prompt'],
                                  pexpect.EOF,
                                  pexpect.TIMEOUT,
                                  'assword:',
                                  '\(yes/no\)\?'],
                                 timeout)
        elif 'vpn' == server:
            switch = proc.expect([conf['vpns']['prompt'],
                                  pexpect.EOF,
                                  pexpect.TIMEOUT,
                                  'assword:',
                                  '\(yes/no\)\?'],
                                 timeout)
        elif 'dp' == server:
            switch = proc.expect([conf['dps']['prompt'],
                                  pexpect.EOF,
                                  pexpect.TIMEOUT,
                                  'assword:',
                                  '\(yes/no\)\?'],
                                 timeout)
        elif 'node' == server:
            switch = proc.expect([conf['nodes']['prompt'],
                                  pexpect.EOF,
                                  pexpect.TIMEOUT,
                                  'assword:',
                                  '\(yes/no\)\?'],
                                 timeout)
        else:
            raise Exception("TypeError")
        if 0 == switch:
            return
        elif 1 == switch:
            if not(0 == tcount):
                eof_handler()
                tcount -= 1
            else:
                print('eof failure: %s' % (proc.before))
                raise Exception("TIMEOUT")
        elif 2 == switch:
            if not(0 == tcount):
                timeout_handler()
                tcount -= 1
            else:
                print('timeout failure: %s' % (proc.before))
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
# end of wait_server


def prepare_file(conf, tag):
    """prepare files for vpns, dps"""
    c = pexpect.spawn('bash')
    wait_server(conf, c)

    if ('vpn' == tag):
        c.sendline("if [ ! -d 'tovpn'    ];then mkdir tovpn;fi")
        wait_server(conf, c)
        for s in conf['tovpn']:
            c.sendline('cp %s ./tovpn' % (os.path.join(conf['test_lib_dir'], s)))
            wait_server(conf, c)
            if not(c.before.find('cannot') == -1):
                print('prepare_file failure: ', c.before)
                raise Exception(c.before)

    elif('dp' == tag):
        c.sendline("if [ ! -d 'todp'    ];then mkdir todp;fi")
        wait_server(conf, c)
        for s in conf['todp']:
            c.sendline('cp %s ./todp' % (os.path.join(conf['test_lib_dir'], s)))
            wait_server(conf, c)
            if not(c.before.find('cannot') == -1):
                print('prepare_file failure: ', c.before)
                raise Exception(c.before)
    else:
        print('failure: unknown server: %s' % (tag))
        raise Exception('unknown server:', tag)
# end of prepare_file


def get_time_region(cur_time):
    """for given cur_time, return cur_region which include cur_time,\
            return opp_region which not include cur_time"""
    cur_region_l = time.gmtime(cur_time + 22 * 3600)
    cur_region_r = time.gmtime(cur_time +  2 * 3600)
    opp_region_l = time.gmtime(cur_time + 10 * 3600)
    opp_region_r = time.gmtime(cur_time + 14 * 3600)

    return "%s-%s" % (time.strftime('%H:%M', cur_region_l), time.strftime('%H:%M', cur_region_r)),\
        "%s-%s" % (time.strftime('%H:%M', opp_region_l), time.strftime('%H:%M', opp_region_r))
# end of get_time_region


def get_vpn_no(conf):
    import pexpect
    c = pexpect.spawn('bash')
    c.expect('\$')
    vpns = conf['vpns']
    for k in vpns:
        if (k == 'prompt') | (k == 'pswd'):
            continue
        if not(c.before.find(vpns[k]['name']) == -1):
            return k

    return None
# end of get_vpn_no


def get_dp_no(conf):
    import pexpect
    c = pexpect.spawn('bash')
    c.expect('\$')
    dps = conf['dps']
    for k in dps:
        if (k == 'prompt') | (k == 'pswd'):
            continue
        if not(c.before.find(dps[k]['name']) == -1):
            return k

    return None
# end of get_dp_no

def set_vworker_mode(_conf,
                     ssh_dpsvr_proc,
                     _node_seq_no,
                     _mode
                    ):
    """
    @param _conf: test configuration
    @param ssh_dpsvr_proc: the ssh subprocess to dp server which\
            related to [_node_seq_no]th test device
    @param _node_seq_no: the sequence number of current test device\
            in _conf['nodes']
    @param _mode: video worker mode to be setted
    @return None
    @raise
    @Author: Yifei.Fu
    """
    if('install' == _mode):
        new_conf_str = str({"installation-mode": "yes"})
    elif('tracking' == _mode):
        new_conf_str = str({"installation-mode": "no", "capture-mode": "tracking"})
    elif('loi' == _mode):
        new_conf_str = str({"installation-mode": "no", "capture-mode": "loi"})
    elif('video' == _mode):
        new_conf_str = str({"installation-mode": "no", "capture-mode": "video"})
    elif('zone-count' == _mode):
        new_conf_str = str({"installation-mode": "no", "capture-mode": "zone-count"})
    else:
        print("set video worker mode failure, illegal mode name:%s" % _mode)
        raise NameError("Wrong mode name.")

    ssh_dpsvr_proc.sendline("python update_config.py %s \"%s\"" %
                            (_conf['nodes'][_node_seq_no]['name'], new_conf_str)
                           )
    wait_server(_conf, ssh_dpsvr_proc, 'dp')
    if not(ssh_dpsvr_proc.before.find('failure') == -1):
        print('update config failure: %s' % (ssh_dpsvr_proc.before))
        raise Exception('update config failure')
    elif not(ssh_dpsvr_proc.before.find('success') == -1):
        print('update config ok.')
    else:
        print('abortion failure: %s')
        print(ssh_dpsvr_proc.before)
        raise Exception('abortion failure')
# end of set_vworker_mode

def chk_vworker_mode(_conf,
                     ssh_dpsvr_proc,
                     _node_seq_no,
                     _mode
                    ):
    """
    @param _conf: test configuration
    @param ssh_dpsvr_proc: the ssh subprocess to dp server which\
            related to [_node_seq_no]th test device
    @param ssh_vpnsvr_proc: the ssh subprocess to vpn server
    @param _node_seq_no: the sequence number of current test device\
            in _conf['nodes']
    @param _mode: video worker mode to be setted
    @Author: Yifei.Fu
    """
    if('install' == _mode):
        svr_data_dir = os.path.join(_conf['svr_video_dir'],
                                    _conf['nodes'][_node_seq_no]['name']
                                   )
        waiting_time = 1
    elif('tracking' == _mode):
        svr_data_dir = os.path.join(_conf['svr_blob_dir'],
                                    _conf['nodes'][_node_seq_no]['name']
                                   )
        waiting_time = 2
    elif('loi' == _mode):
        svr_data_dir = os.path.join(_conf['svr_blob_dir'],
                                    _conf['nodes'][_node_seq_no]['name']
                                   )
        waiting_time = 2
    elif('video' == _mode):
        svr_data_dir = os.path.join(_conf['svr_video_dir'],
                                    _conf['nodes'][_node_seq_no]['name']
                                   )
        waiting_time = 25
    elif('zone-count' == _mode):
        svr_data_dir = os.path.join(_conf['svr_zc_dir'],
                                    _conf['nodes'][_node_seq_no]['name']
                                   )
        waiting_time = 3
    else:
        print("chk video worker mode failure, illegal mode name:%s" % _mode)
        raise NameError("Wrong mode name.")

    curTime = time.time()
    ssh_dpsvr_proc.sendline("python get_file_num.py %s %s %s" %
                            (svr_data_dir,
                             _mode,
                             curTime
                            )
                           )
    wait_server(_conf, ssh_dpsvr_proc, 'dp', 180)
    if(ssh_dpsvr_proc.before.find('##number##') == -1):
        print('get_file_num failure: %s' % (ssh_dpsvr_proc.before))
        raise Exception('get_file_num failure')
    tmpList = ssh_dpsvr_proc.before.split('##')
    num1 = int(tmpList[tmpList.index('number') + 1])

    #waiting for mode switching
    _counter1 = 40 # 40*30 seconds
    while(_counter1 > 0):
        ssh_dpsvr_proc.sendline("python check_module_mode.py '%s' \"%s\"" %
                                (_conf['nodes'][_node_seq_no]['name'],
                                 str({"video": {"mode": _mode}})
                                )
                               )
        wait_server(_conf, ssh_dpsvr_proc, 'dp')
        if not(ssh_dpsvr_proc.before.find('success') == -1):
            print('check_module_mode success.')
            break
        else:
            _counter1 -= 1
            print('try %s times.' % (str(40 - _counter1)))
            time.sleep(30)
    if(0 == _counter1):
        print('check_module_mode failure: %s' % (ssh_dpsvr_proc.before))
        raise Exception('check_module_mode failure')

    #waiting for data generating and uploading
    # if waiting to long, the dp server may force terminating the connection.
    # time.sleep(waiting_time)-----> deprecated for connectivity issue

    _counter2 = 60 # 60*30 seconds
    _counter2 += waiting_time
    while(_counter2 > 0):
        ssh_dpsvr_proc.sendline("python get_file_num.py %s %s %s" %
                                (svr_data_dir,
                                 _mode,
                                 curTime
                                )
                               )
        wait_server(_conf, ssh_dpsvr_proc, 'dp', 180)
        if(ssh_dpsvr_proc.before.find('##number##') == -1):
            print('get_file_num failure: %s' % (ssh_dpsvr_proc.before))
            raise Exception('get_file_num failure')
        tmpList = ssh_dpsvr_proc.before.split('##')
        num2 = int(tmpList[tmpList.index('number') + 1])

        if (num1 < num2):
            print('chk_vworker_mode success')
            break
        else:
            _counter2 -= 1
            time.sleep(30)

    if(0 == _counter2):
        print('check_vworker_mode failure: %s')
        print(ssh_dpsvr_proc.before)
        raise Exception('check_vworker_mode failure')
#end of chk_vworker_mode


