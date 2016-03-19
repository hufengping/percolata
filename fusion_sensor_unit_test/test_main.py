#!/usr/bin/env python

# created by Yifei.Fu at 2015-01-20
# this is the test entrance for bs-embedded-dev of percolata.com
"""what should be added for module docstring"""


import os
import sys
import logging
import time
import inspect
import pexpect
import json

# set config file dir/name
CONFIG_FILE = './config_test.json'

# set log level, 'WARN' == prefered
LOG_LEVEL = logging.DEBUG


def get_script_dir():
    """return the abspath of current script."""
    self = inspect.stack()[0][1]
    return os.path.abspath(os.path.dirname(self))
# end of get_script_dir


def choose_test_type(arg):
    """select test type: 'ci', 'ft', 'uat',
    'debug_test' only for debugging test procedure"""
    if 'ci' == arg:
        pexpect.run("cp -f ./TestTemplates/ci_list_test.json list_test.json")
    elif 'ft' == arg:
        pexpect.run("cp -f ./TestTemplates/ft_list_test.json list_test.json")
    elif 'uat' == arg:
        pexpect.run("cp -f ./TestTemplates/uat_list_test.json list_test.json")
    elif 'debug_test' == arg:
        pexpect.run("cp -f ./TestTemplates/debug_list_test.json list_test.json")
    else:
        raise Exception("Error: wrong test type:%s" % (arg))
# end of choose_arg


def set_log(log_filename, log_init_message):
    """generate a test log."""
    _logger = logging.getLogger()
    handler = logging.FileHandler(log_filename)
    _logger.addHandler(handler)
    _logger.setLevel(LOG_LEVEL)
    _logger.info(log_init_message)
    return _logger
# end of set_log


def parse_config(filename):
    """decode config from json file."""
    _conf = {}

    try:
        with open(filename, 'r') as config:
            flogger(logger, 'info', 'start analyse CONFIG_FILE for test.\n')
            # parse CONFIG_FILE
            _conf = json.load(config)
    except IOError as err:
        flogger(logger, 'error', '%s' % err)
        raise Exception("cannot open config file.")
    return _conf
# end of parse_config


def parse_test_list(filename):
    """decode config from json file."""
    _test_list = {}

    try:
        with open(filename, 'r') as test_list_file:
            flogger(logger, 'info', 'start analyse test_list_file for test.\n')
            # parse _test_list file
            _test_list = eval(test_list_file.read().strip())
    except IOError as err:
        flogger(logger, 'error', '%s' % err)
        raise Exception("cannot open test_list_file.")
    return _test_list
# end of parsetest_list_file


def flogger(_logger, level, msg):
    """log recoder."""
    if level == 'info':
        _logger.info(
            '%s.in file:%s at line:%s: ==[INFO]==' %
            (time.strftime("%H:%M:%S_%m-%d-%Y"),
             c.f_code.co_filename,
             c.f_lineno) +
            msg)
    elif level == 'warn':
        _logger.warn(
            '%s.in file:%s at line:%s: ==[WARN]==' %
            (time.strftime("%H:%M:%S_%m-%d-%Y"),
             c.f_code.co_filename,
             c.f_lineno) +
            msg)
    elif level == 'error':
        _logger.error(
            '%s.in file:%s at line:%s: ==[ERROR]==' %
            (time.strftime("%H:%M:%S_%m-%d-%Y"),
             c.f_code.co_filename,
             c.f_lineno) +
            msg)
    elif level == 'critical':
        _logger.critical(
            '%s.in file:%s at line:%s: ==[FATAL]==' %
            (time.strftime("%H:%M:%S_%m-%d-%Y"),
             c.f_code.co_filename,
             c.f_lineno) +
            msg)
    elif level == 'debug':
        _logger.debug(
            '%s.in file:%s at line:%s: ==[DEBUG]==' %
            (time.strftime("%H:%M:%S_%m-%d-%Y"),
             c.f_code.co_filename,
             c.f_lineno) +
            msg)
    elif level == 'add':
        _logger.info('\t\t\t%s' % (msg))
    else:
        flogger(_logger, 'warn', 'wrong use with logging level.')
# end of flogger


def search_script(script_id, search_dir):
    """Oops,forgot something."""
    if script_id in search_dir[1]:
        return os.path.join(search_dir[0], script_id)
    else:
        return None
# end of search_script

def eof_handler():
    """this function is used to handle EOF events while waiting response from remotes"""
    flogger(logger, 'info', 'eof_handler:EOF with response.')
# end of timeout_handler

def timeout_handler(count):
    """this function is used to handle timeout events while waiting response from remotes"""
    flogger(logger, 'info', 'timeout_handler:%sth time segment with running script.' % (count))
# end of timeout_handler


def wait_server(_conf, proc, server='local', timeout=60):
    """interact with remotes."""
    time.sleep(0.1)
    # avoid dead loop
    _tcount = 3
    while True:
        if 'local' == server:
            switch = proc.expect([_conf['prompt'],
                                  pexpect.EOF,
                                  pexpect.TIMEOUT,
                                  'assword:',
                                  '\(yes/no\)\?'],
                                 timeout)
        elif 'vpn' == server:
            switch = proc.expect([_conf['vpns']['prompt'],
                                  pexpect.EOF,
                                  pexpect.TIMEOUT,
                                  'assword:',
                                  '\(yes/no\)\?'],
                                 timeout)
        elif 'dp' == server:
            switch = proc.expect([_conf['dps']['prompt'],
                                  pexpect.EOF,
                                  pexpect.TIMEOUT,
                                  'assword:',
                                  '\(yes/no\)\?'],
                                 timeout)
        elif 'node' == server:
            switch = proc.expect([_conf['nodes']['prompt'],
                                  pexpect.EOF,
                                  pexpect.TIMEOUT,
                                  'assword:',
                                  '\(yes/no\)\?'],
                                 timeout)
        else:
            raise Exception("wrong server type")
        if 0 == switch:
            return
        elif 1 == switch:
            if not 0 == _tcount:
                eof_handler()
                _tcount -=1
            else:
                print('eof failure: %s' % proc.before)
                raise Exception(proc.before)
        elif 2 == switch:
            if not 0 == _tcount:
                timeout_handler(_tcount)
                _tcount -= 1
            else:
                print('timeout failure: %s' % proc.before)
                raise Exception(proc.before)
        elif 3 == switch:
            if not 0 == _tcount:
                proc.sendline(_conf['nodes']['pswd'])
                _tcount -= 1
            else:
                print('login failure')
                raise Exception(proc.before)
        elif 4 == switch:
            proc.sendline('yes')
# end of wait_server


def prepare_file(_conf, tag):
    """prepare files for vpns, dps"""
    ssh_proc = pexpect.spawn('bash')
    wait_server(_conf, ssh_proc)

    if  'vpn' == tag:
        ssh_proc.sendline("if [ ! -d 'tovpn'    ];then mkdir tovpn;fi")
        wait_server(_conf, ssh_proc)
        for elem in _conf['tovpn']:
            ssh_proc.sendline('cp %s ./tovpn' % (os.path.join(_conf['test_lib_dir'], elem)))
            wait_server(_conf, ssh_proc)
            if not ssh_proc.before.find('cannot') == -1:
                print('prepare_file failure: ', ssh_proc.before)
                raise Exception(ssh_proc.before)

    elif 'dp' == tag:
        ssh_proc.sendline("if [ ! -d 'todp'    ];then mkdir todp;fi")
        wait_server(_conf, ssh_proc)
        for elem in _conf['todp']:
            ssh_proc.sendline('cp %s ./todp' % (os.path.join(_conf['test_lib_dir'], elem)))
            wait_server(_conf, ssh_proc)
            if not ssh_proc.before.find('cannot') == -1:
                print('prepare_file failure: ', ssh_proc.before)
                raise Exception(ssh_proc.before)
    else:
        print('failure: unknown server: %s' % tag)
        raise Exception('unknown server:', tag)
# end of prepare_file


def restore_env(_conf, _logger):  # To Be Improve Continually
    """restore configuration on each test dp for each test device"""
    workdir = get_script_dir()
    for dp in _conf['dps']:
        if  dp == 'prompt':
            continue
        prepare_file(_conf, 'dp')
        ssh_restore_proc = pexpect.spawn("ssh %s" % (_conf['dps'][dp]['ssh']))
        wait_server(_conf, ssh_restore_proc, 'dp')
        ssh_restore_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
        wait_server(_conf, ssh_restore_proc, 'dp')
        tmp_proc = pexpect.spawn("bash")
        wait_server(_conf, tmp_proc)
        tmp_proc.sendline('scp -r %s/todp/* %s:./TestBench' % (workdir, _conf['dps'][dp]['ssh']))
        wait_server(_conf, tmp_proc)
        tmp_proc.close(force=True)
        ssh_restore_proc.sendline("python restore_config.py ")
        wait_server(_conf, ssh_restore_proc, 'dp')
        if not ssh_restore_proc.before.find('failure') == -1:
            flogger(_logger, 'info', 'restorEnv failure.--->%s' % (ssh_restore_proc.before))
        ssh_restore_proc.close(force=True)
# end of restore_env


if __name__ == '__main__':
    """main entrance for test, Accept one optional command line arguement,'debug_test' by default
    e.g.  ./test_main.py [XXX];  XXX can be 'ci' or 'uat' or 'ft' or 'debug_test' or 'alph'
    after test procedure, the output log will be put into the current work dir"""
    c = inspect.currentframe()

    SELF_DIR = get_script_dir()
    os.chdir(SELF_DIR)

    TIMESTR = time.strftime("%H_%m-%d-%Y")
    logger = set_log("test_log", "start test at %s" % (TIMESTR))

    # handle config file
    conf = parse_config(CONFIG_FILE)
    conf['test_base_dir'] = SELF_DIR
    conf['test_lib_dir'] = os.path.join(SELF_DIR, 'TestLibs')

    # choose_test_type: 'ci','ft','uat','alph'
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = conf['test_type']

    choose_test_type(test_type)

    # hanle test_list file
    try:
        test_list = parse_test_list(conf["test_list_file"])
    except KeyError as err:
        flogger(logger, 'error', 'KeyError: the key %s == not exist\n' % err)
    # exec scripts and gather reports
    for (tc, args) in test_list.items():
        tcount = 0
        for target in os.walk(os.getcwd() + os.sep + 'TestScripts' + os.sep):
            match = search_script(tc, target)
            if not match is None:
                script = os.path.join(match, tc + '.py')
                # only exec the first found script
                if 0 == tcount:
                    if os.path.isfile(script):
                        # call the target script
                        flogger(logger, 'info', 'start run %s' % (script))
                        print(
                            "start testing %s..." %
                            script)
                        try:
                            retbuf = pexpect.run('python %s %s "%s"' %
                                                 (script, match, str(conf)),\
                                                 events={pexpect.TIMEOUT: timeout_handler},\
                                                 timeout=3600)
                        except Exception as err:
                            flogger(logger, 'error', 'err:%s with running %s' % (err, script))
                        # analyse reports
                        else:
                            if not retbuf.find('failure') == -1:
                                flogger(
                                    logger, 'error', 'run %s with failure=====>\n%s' %
                                    (script, retbuf))
                                # restore env: as testscripts may exit
                                #    without restoring all changes that have been drawn into
                                #    the enviroment
                                restore_env(conf, logger)
                            elif not retbuf.find('success') == -1:
                                flogger(
                                    logger, 'info', 'run %s successfully=====>\n%s' %
                                    (script, retbuf))
                            else:
                                flogger(
                                    logger, 'error', 'unknow status of %s=====>\n%s' %
                                    (script, retbuf))
                                restore_env(conf, logger)

                        flogger(logger, 'info', 'finish  %s.\n' % (script))
                        tcount += 1
                    else:
                        flogger(logger, 'error', 'target script:%s not exist.\n' % (script))
                else:
                    flogger(logger, 'warn', 'replicated script:%s.\n' % (script))
    flogger(logger, 'info', 'finished test.\n')
# end of __main__
