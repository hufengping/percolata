#!/usr/bin/env python
#created by Yifei.Fu at 2015-01-21

import os,sys,pexpect,time,tempfile
import json

config_file = './config_test.json'



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

def cmpDict(devConf, expConf):
    try:
        for k in expConf:
            if(type(expConf[k]).__name__ == 'dict'):
                if(cmpDict(devConf[k],expConf[k]) == -1):
                    return -1
            else:
                if not(cmp(devConf[k],expConf[k]) == 0):
                    return -1
    except Exception as err:
        return -1
    else:
        return 0
#end of cmpDict

if __name__ == '__main__':
    """check specified node's module status from vpn server
    sys.argv[1] specify the device name
    sys.argv[2] specify the expected device configurations"""
    conf = parse_config(config_file)
    from interact import *

    devName = sys.argv[1]
    expConf = eval(sys.argv[2])

    #get devConf
    c = pexpect.spawn('bash')
    wait_server(conf,c,'vpn')
    nodes = conf['nodes']
    for node in nodes:
        if(node == 'prompt')|(node == 'pswd'):
            continue
        if(devName == nodes[node]['name']):
            c.sendline('scp -P 443 %s:%s %s.json'%(nodes[node]['ssh'],\
                    os.path.join(conf['dev_conf_dir'],'fusion-sensor.json'),\
                    devName))
            wait_server(conf,c,'vpn')
            break

    devConf = parse_config('%s.json'%(devName))

    #checking
    if(cmpDict(devConf,expConf) == -1):
        print("check config failure.\n")
    else:
        print('check config successful.\n')

    c.close(force=True)
