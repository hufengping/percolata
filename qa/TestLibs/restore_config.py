#!/usr/bin/env python
#created by Yifei.Fu at 2015-01-21

import os,sys,pexpect,time
import json,re,glob
config_file = './config_test.json'

def get_script_dir():
    self = inspect.stack()[0][1]
    return os.path.abspath(os.path.dirname(self))
#end of get_script_dir

def parse_config(filename):
    configurations = {}

    try:
        with open(filename,'r') as config:
            #parse config_file
            configurations = json.load(config)
    except IOError as err:
        print('open config file failure.\n')
        raise Exception("undefined exception.")
    return configurations
#end of parse_config

if __name__ == '__main__':
    """restore devices' config on dp server
    sys.argv[1]: placement_name     --> devName
    """
    self_dir = get_script_dir()
    os.chdir(self_dir)
    conf = parse_config(config_file)
    from interact import *

    #devName = sys.argv[1]
    devNameRegex = re.compile(r'([1-9]{2})0{2,4}([1-9]\d{0,2})')
    regex1 = re.compile(r'bak_(.*)?.json')
    for e in glob.glob('bak_*.json'):
        m1 = regex1.match(e)
        m  = devNameRegex.match(m1.group(1))
        if not(None == m):
            oldConFile = os.path.join(conf['svr_conf_dir'],m.group()+'.json')
            #restore original device configuration with bak_XXXXXXX.json
            pexpect.run('touch %s'%e)
            pexpect.run('mv -f %s %s '%(e,oldConFile))
        elif ("updateAdminConfig" == m1.group(1)):
            continue #don't restore this config
        elif ("updateSensorConfig" == m1.group(1)):
            continue #don't restore this config
        else:#TOBE ADD NEW OPTION HERE
            pass

