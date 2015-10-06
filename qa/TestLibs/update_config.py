#!/usr/bin/env python
#created by Yifei.Fu at 2015-01-21

import os,sys,pexpect,time,re
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

if __name__ == '__main__':
    """update devices' config on dp server
    sys.argv[1]: target --> devName, or officeUpdateConfig, or ...
    sys.argv[2]: new configurations --> newConf
    """
    conf = parse_config(config_file)
    from interact import *

    devNameRegex = re.compile(r'([1-9]{2})0{2,4}([1-9]\d{0,2})')
    if not(None == devNameRegex.match(sys.argv[1])):
        oldConFile = os.path.join(conf['svr_conf_dir'],sys.argv[1]+'.json')
    elif ("updateAdminConfig" == sys.argv[1]):
        oldConFile = conf['updateAdminConfig']
    elif ("updateSensorConfig" == sys.argv[1]):
        oldConFile = conf['updateSensorConfig']
    else:#TOBE ADD NEW OPTION HERE
        pass

    newConf = eval(sys.argv[2])

    mergeDict = lambda d1,d2:{k:d1[k] if not k in d2 \
            else mergeDict(d1[k],d2[k]) if (k in d1 and\
                type(d1[k]).__name__ == 'dict' and\
                type(d2[k]).__name__ == 'dict')\
                else d2[k] for k in set(d1)|set(d2)}

    #get original device configuration
    #first backup it, then modify it
    if os.path.isfile(oldConFile):
        if not os.path.isfile('./bak_%s.json'%sys.argv[1]):
            ret=pexpect.run('cp %s ./bak_%s.json'%\
                    (oldConFile,sys.argv[1]))
            if not os.path.isfile('./bak_%s.json'%sys.argv[1]):
                print("backup device config file failure: %s"%ret)
                raise Exception("backup config failure.")
    try:
        with open(oldConFile,'r+') as fp:
            #parse config_file
            oldConf = json.load(fp)
            #merge oldConf with newConf
            _updatedConf = mergeDict(oldConf, newConf)
            #write back to device config file
            fp.seek(0)
            fp.truncate()
            json.dump(_updatedConf,fp,sort_keys=True)
    except IOError as err:
        print('open config failure.\n')
        raise Exception("update config failure.")

    #report
    print('update config success.\n')
