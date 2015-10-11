#!/usr/bin/env python

import os
import json
import time

# constants
ROOT_DIR = "/data/software"
APK_NAME = "FusionSensor"
APK_DIR =  "moto-fusion-sensor"
TEST_APK_PATH = "./test_software/FusionSensor_test.apk"
UPDATE_CONFIG_SCRIPT = "./fusion_sensor_upgrade.py"
TEST_PLACEMENT_CONFIG_FILE = "/data/config/8100031.json"

# change to script directory
os.chdir(ROOT_DIR)

# copy a fake upgrade app to the certain directory
# copy command: "cp {SRC_PTH} {DST_PTH}"
os.system("cp %s %s/%s.apk" % (TEST_APK_PATH, APK_DIR, APK_NAME))

# execute the update config script
os.system(UPDATE_CONFIG_SCRIPT)

def modifyUpgradeMode(upgradeMode):
    # parse json file
    config_file = file(TEST_PLACEMENT_CONFIG_FILE)
    json_obj = json.load(config_file) 
    #print json_obj
    
    # modify update mode
    sw_update_node = json_obj["softwareUpdate"]
    sw_update_node["forceUpdate"] = upgradeMode
    
    # save modified json file
    with open(TEST_PLACEMENT_CONFIG_FILE, "w") as config_file:
        json.dump(json_obj, config_file, sort_keys=True)


if os.path.exists(TEST_PLACEMENT_CONFIG_FILE):
    # modify the placement config file to notify upgrade
    modifyUpgradeMode("true") 
    
    time.sleep(10 * 60)
    
    # resume the placement config file
    modifyUpgradeMode("false") 
        
    # test over
       
else:
    # need create a config file with default value  
    pass  










 
