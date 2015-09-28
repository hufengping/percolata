#!/usr/bin/env python
#created by Yifei.Fu at 2015-01-21

import os,sys,tempfile
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
    """check specified node's module status from vpn server
    sys.argv[1] specify the placement name
    sys.argv[2] specify the list of module names
    """
    conf = parse_config(config_file)
    from interact import *
    from time import *
    from pexpect import *
    devName = sys.argv[1] #get placement name from argv
    _myNo = get_dp_no(conf)
    if (_myNo == None):
        print("get dp no failure: unknown dp server.\n")
        raise Exception("undefined exception.")
    #check all modules by default
    chkList = ['log','config','upload','upgrade','sysmon','video','wifi','wificontrol','openvpn','websocket']
    if(len(sys.argv) >= 3):
        buf=eval(sys.argv[2])#get module names which need to be checked
        if not(type(buf).__name__ == 'list'):
            print("wrong checklist failure,please check the 2nd arguement for check_module_health.py")
            raise Exception("undefined exception.")
        else:
            chkList = buf

    c = spawn('bash')
    c.expect('%s'%(conf['dps'][_myNo]['prompt']))
    c.sendline('cat /log/placement_%s.txt |grep status|tail -1'%(devName))
    c.expect('%s'%(conf['dps'][_myNo]['prompt']))
    heartbeat = c.before.strip()
    statusList = heartbeat.split('|')

    for item in chkList:
        try:
            if(item == 'log'):
                #we say, the log module == ok when its latest heartbeat came later than 20min at past.
                time_lim = strftime('%Y-%m-%d %H:%M:%S',gmtime(time()-1200))
                index = statusList.index('FS-status')
                time_rcv = statusList[index-2]
                if(time_rcv < time_lim):
                    print('check log module failure.\n')
                    raise Exception("undefined exception.")
            elif(item == 'config'):
#TODO
                pass
            elif(item == 'upload'):
#TODO improvement
                #currently, check left list has no less than 2 zeros, e.g. "Left:1*0*0*0"
                index = statusList.index('BS-uploader')
                tag = statusList[index+1].split(',')[0].split(':')[1].split('*')
                count = 0
                for e in tag:
                    if(e == '0'):
                        count += 1;
                if(count <= 1):
                    print('check upload module failure.\n')
                    raise Exception("check upload module failure.")
            elif(item == 'upgrade'):
                index = statusList.index('BS-update')
                tag = statusList[index+1]
                if not(tag[0] == 'Y' or tag[0] == 'N'):
                    print('check upgrade module failure.\n')
                    raise Exception("check upgrade module failure.")
            elif(item == 'sysmon'):
                pass
#               index = statusList.index('BS-sysmon')
#               tag = statusList[index+1]
#               if not(tag[0] == 'C'):
#                   print('check sysmon module failure.\n')
#                   raise Exception("undefined exception.")
            elif(item == 'video'):
                index = statusList.index('BS-video')
                tag = statusList[index+1].split()
                if not((tag[-1] == "STATE_STARTED") or (tag[-1] == "sleeping")):
                    print('check video module failure.\n')
                    raise Exception("check video module failure.")
            elif(item == 'wifi'):
                index = statusList.index('BS-wifi')
                tag = statusList[index+1].split()
                if not(tag[2] == "true"):
                    print('check wifi module failure.\n')
                    raise Exception("check wifi module failure.")
            elif(item == 'wificontrol'):
                index = statusList.index('BS-wificontrol')
                tag = statusList[index+1]
                if not(tag[0] == 'U'):
                    print('check wificontrol module failure.\n')
                    raise Exception("check wificontrol module failure.")
            elif(item == 'openvpn'):
                index = statusList.index('BS-openvpn')
                tag = statusList[index+1]
                if not(tag == 'yes'):
                    print('check openvpn module failure.\n')
                    raise Exception("check openvpn module failure.")
            elif(item == 'websocket'):
                index = statusList.index('BS-websocket')
                tag = statusList[index+1]
                if not(tag == 'yes'):
                    print('check websocket module failure.\n')
                    raise Exception("check websocket module failure.")
            else:
                #unsurported module
                pass
        except Exception as err:
            print("unexpected failure while checking heartbeat with %s : %s"%(item,err))
            raise Exception("%s."%err)


    #report
    print('check module health successful.\n')

    #release subprocess
    c.close(force=True)
