#!/usr/bin/env python

#created by Yifei.Fu at 2015-01-20
#this is the test entrance for bs-embedded-dev of percolata.com



import os, sys, logging, time, inspect, pexpect, json

#set config file dir/name
config_file = './config_test.json'

#set log level, 'WARN' == prefered
log_level = logging.DEBUG

def get_script_dir():
    self = inspect.stack()[0][1]
    return os.path.abspath(os.path.dirname(self))
#end of get_script_dir

def choose_test_type(test_type):
    # select test type: 'ci', 'ft', 'uat',
    # 'debug_test' only for debugging test procedure
    if ('ci' == test_type):
        ret = pexpect.run("cp -f ./TestTemplates/ci_list_test.json list_test.json")
    elif ('ft' == test_type):
        ret = pexpect.run("cp -f ./TestTemplates/ft_list_test.json list_test.json")
    elif ('uat' == test_type):
        ret = pexpect.run("cp -f ./TestTemplates/uat_list_test.json list_test.json")
    elif ('debug_test' == test_type):
        ret = pexpect.run("cp -f ./TestTemplates/debug_list_test.json list_test.json")
    else:
        raise Exception("Error: wrong test type:%s"%(test_type))
#end of choose_test_type


def setLog(log_filename, log_init_message):
    logger = logging.getLogger()
    handler= logging.FileHandler(log_filename)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    logger.info(log_init_message)
    return logger
#end of setLog

def parse_config(filename):
    conf = {}

    try:
        with open(filename,'r') as config:
            flogger(logger,'info','start analyse config_file for test.\n')
            #parse config_file
            conf = json.load(config)
    except IOError as err:
        flogger(logger,'error','%s'%err)
        raise Exception("undefined exception.")
    return conf
#end of parse_config

def parse_test_list(filename):
    test_list = {}

    try:
        with open(filename,'r') as _test_list:
            flogger(logger,'info','start analyse test_list_file for test.\n')
            #parse test_list file
            test_list = eval(_test_list.read().strip())
    except IOError as err:
        flogger(logger,'error','%s'%err)
        raise Exception("undefined exception.")
    return test_list
#end of parse_test_list

def flogger(logger,level, msg):
    if level == 'info':
        logger.info('%s.in file:%s at line:%s: ==[INFO]=='%(time.strftime("%H:%M:%S_%m-%d-%Y"),c.f_code.co_filename, c.f_lineno)+msg)
    elif level == 'warn':
        logger.warn('%s.in file:%s at line:%s: ==[WARN]=='%(time.strftime("%H:%M:%S_%m-%d-%Y"),c.f_code.co_filename, c.f_lineno)+msg)
    elif level == 'error':
        logger.error('%s.in file:%s at line:%s: ==[ERROR]=='%(time.strftime("%H:%M:%S_%m-%d-%Y"),c.f_code.co_filename, c.f_lineno)+msg)
    elif level == 'critical':
        logger.critical('%s.in file:%s at line:%s: ==[FATAL]=='%(time.strftime("%H:%M:%S_%m-%d-%Y"),c.f_code.co_filename, c.f_lineno)+msg)
    elif level == 'debug':
        logger.debug('%s.in file:%s at line:%s: ==[DEBUG]=='%(time.strftime("%H:%M:%S_%m-%d-%Y"),c.f_code.co_filename, c.f_lineno)+msg)
    elif level == 'add':
        logger.info('\t\t\t%s'%(msg))
    else:
        flogger(logger,'warn','wrong use with logging level.')
#end of flogger


def search_script(script_id, search_dir):
    if(script_id in search_dir[1]):
        return os.path.join(search_dir[0],script_id)
    else:
        return None
#end of search_script


def timeout_handler(count):
    flogger(logger,'info','timeout_handler:%sth time segment with running script.'%(count))
#end of timeout_handler

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
            raise Exception("wrong server type")
        if 0 == switch:
            return
        elif 1 == switch:
            eof_handler()
        elif 2 == switch:
            if not(0 == tcount):
                timeout_handler(tcount)
                tcount -= 1
            else:
                print('timeout failure: %s'%(proc.before))
                raise Exception(proc.before)
        elif 3 == switch:
            if not(0 == tcount):
                proc.sendline(conf['nodes']['pswd'])
                tcount -= 1
            else:
                print('login failure')
                raise Exception(proc.before)
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

def restoreEnv(conf,logger):  #To Be Improve Continually
    #restore configuration on each test dp for each test device
    workdir = get_script_dir()
    for dp in conf['dps']:
        if (dp == 'prompt'):
            continue
        prepare_file(conf,'dp')
        ssh_restore_proc = pexpect.spawn("ssh %s"%(conf['dps'][dp]['ssh']))
        wait_server(conf,ssh_restore_proc,'dp')
        ssh_restore_proc.sendline("if [ ! -d 'TestBench'  ];then mkdir TestBench;fi;cd TestBench")
        wait_server(conf,ssh_restore_proc,'dp')
        tmp_proc = pexpect.spawn("bash")
        tmp_proc.sendline('scp -r %s/todp/* %s:./TestBench'%(workdir,conf['dps'][dp]['ssh']))
        wait_server(conf,tmp_proc)
        tmp_proc.close(force=True)
        ssh_restore_proc.sendline("python restore_config.py ")
        wait_server(conf,ssh_restore_proc,'dp')
        if not(ssh_restore_proc.before.find('failure') == -1):
            flogger(logger,'info','restorEnv failure.--->%s'%(ssh_restore_proc.before))
        ssh_restore_proc.close(force=True)
#end of restoreEnv


if __name__ == '__main__':
    """main entrance for test, Accept one optional command line arguement,'debug_test' by default
    e.g.  ./test_main.py [XXX];  XXX can be 'ci' or 'uat' or 'ft' or 'debug_test' or 'alph'
    after test procedure, the output log will be put into the current work dir"""
    c = inspect.currentframe()

    self_dir = get_script_dir()
    os.chdir(self_dir)

    timestr = time.strftime("%H_%m-%d-%Y")
    logger  = setLog("test_log", "start test at %s"%(timestr))

    # handle config file
    conf = parse_config(config_file)
    conf['test_base_dir'] = self_dir
    conf['test_lib_dir'] = os.path.join(self_dir,'TestLibs')

    # choose_test_type: 'ci','ft','uat','alph'
    if(len(sys.argv) > 1):
        test_type = sys.argv[1]
    else:
        test_type = conf['test_type']

    choose_test_type(test_type)

    # hanle test_list file
    try:
        test_list = parse_test_list(conf["test_list_file"])
    except KeyError as err:
        flogger(logger,'error','KeyError: the key %s == not exist\n'%err)
    # TODO restore version check
    # update scripts with remote repository
    #ret = pexpect.run('git pull')
    #ret = pexpect.run('git checkout')

    #if not(ret.find('up-to-date') == -1):
    #    flogger(logger,'info','local scripts updated.\n')
    #else:
    #    pass
    # exec scripts and gather reports
    for (tc,args) in test_list.items():
        tcount = 0
        for dir in os.walk(os.getcwd()+os.sep+'TestScripts'+os.sep):
            match = search_script(tc,dir)
            if not(match == None):
                script = os.path.join(match,tc+'.py')
                #only exec the first found script
                if 0 == tcount:
                    if os.path.isfile(script):
                        #call the target script
                        flogger(logger,'info','start run %s'%(script))
                        print("start testing %s, it will take several minutes,please wait patiently."%script)
                        try:
                            retbuf = pexpect.run('python %s %s "%s"'%\
                                    (script,match,str(conf)),events={pexpect.TIMEOUT:timeout_handler},timeout=3600)
                        except Exception as err:
                            flogger(logger,'error','err:%s with running %s'%(err,script))
                        #analyse reports
                        else:
                            if not(retbuf.find('failure') == -1):
                                flogger(logger,'error','run %s with failure=====>\n%s'%(script,retbuf))
                                #restore env: as testscripts may exit
                                #    without restoring all changes that have been drawn into
                                #    the enviroment
                                restoreEnv(conf,logger)
                            elif not(retbuf.find('success') == -1):
                                flogger(logger,'info','run %s successfully=====>\n%s'%(script,retbuf))
                            else:
                                flogger(logger,'error','unknow status of %s=====>\n%s'%(script, retbuf))
                                restoreEnv(conf,logger)

                        flogger(logger,'info','finish  %s.\n'%(script))
                        tcount += 1
                    else:
                        flogger(logger,'error','target script:%s not exist.\n'%(script))
                else:
                    flogger(logger,'warn','replicated script:%s.\n'%(script))
    flogger(logger,'info','finished test.\n')
#end of __main__
