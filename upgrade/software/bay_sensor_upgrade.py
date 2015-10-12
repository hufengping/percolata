#!/usr/bin/env python

import os
import json
import time
import sys
from optparse import OptionParser

def common_upgrade(constants_json_obj):
    # all kinds of upgrade need
    # get constants
    ROOT_DIR = constants_json_obj['ROOT_DIR']
    SW_UPDATE_DICT = constants_json_obj['SW_UPDATE_DICT']
    APK_DIR = constants_json_obj['APK_DIR']
    APK_INFO_FILE = constants_json_obj['APK_INFO_FILE']

    # change to script directory
    os.chdir(ROOT_DIR)
    #print("Current path: ", os.getcwd())
    
    for apk_name, update_config_file_name in SW_UPDATE_DICT.items():
        apk_file_name = apk_name + ".apk"
        apk_path = os.sep.join([APK_DIR, apk_file_name])
        config_file_dir = APK_DIR
        update_config_file = os.sep.join([APK_DIR, update_config_file_name])
        
        if not os.path.isfile(apk_path):
            print("APK not found: ", apk_file_name)
            continue
        
        if not os.path.isfile(update_config_file):
            print("Config file not found: ", update_config_file)
            continue  
            
        # ensure aapt exits and run well
        # aapt command format "aapt dump badging {APK} > {APK_INFO}"
        aapt_cmd = "sudo aapt dump badging %s > %s" % (apk_path, APK_INFO_FILE)
        #aapt_cmd = "aapt dump badging %s > %s" % (apk_path, APK_INFO_FILE)
        os.system(aapt_cmd)     # print apk info to txt file
        
        if not os.path.exists(APK_INFO_FILE):
            raise IOError("Parse apk info fail. Please check whether the aapt installed.")
  
        with open(APK_INFO_FILE) as info_file:
            # the first line format:
            # package: name='com.baysensors.FusionSensor' versionCode='1' versionName='1.0'
            package_str = info_file.readline()
            
            # get package name
            PACKAGE_NAME_TAG = "name="
            begin_index = package_str.find(PACKAGE_NAME_TAG)
            end_index = package_str.find(" ", begin_index)
            package_name = package_str[begin_index+len(PACKAGE_NAME_TAG)+1:end_index-1]
            
            # get versionName
            VERSION_NAME_TAG = "versionName="
            begin_index = package_str.find("versionName=")
            end_index = package_str.find(" ", begin_index)
            version_name = package_str[begin_index+len(VERSION_NAME_TAG)+1:end_index - 1]
            
        os.remove(APK_INFO_FILE)
        
        # parse json file 
        print "open json file as "+update_config_file
        with open(update_config_file) as sensor_file: 
            json_obj = json.load(sensor_file)
            
        # version format: "version": "08-11-2014.v1.0.0"
        apk_node = json_obj[apk_name]     
        apk_node["version"] = version_name
        apk_node["fileList"] = [apk_file_name]
        apk_node["component"] = apk_name
        apk_node["comPackage"] = package_name
            
        # save modified json file
        with open(update_config_file, "w") as config_file:
            json.dump(json_obj, config_file, sort_keys=True, indent=4)
        # add the md5 of apk to the tail
        update_md5_cmd = "java -jar UpdateMd5CheckSum.jar %s" % update_config_file
        os.system(update_md5_cmd)
        
        print("APK upgrade success: ", apk_file_name.encode('utf8'))
        print("Current version: ", version_name)
        print("Config file updated: ", update_config_file_name.encode('utf8'))  
    

def ci_extra_upgrade(constants_json_obj):
    # CI need more one step
    # get constants
    CI_DEVICE_LIST_JSON = os.sep.join([constants_json_obj['APK_DIR'], constants_json_obj['CI_DEVICE_LIST_JSON']])
    CONFIG_DIR = constants_json_obj['CONFIG_DIR']

    # if the software package is updated, we can force the update happens asap
    # in this case, we need to know which device(s) will perform the update
    if not os.path.exists(CI_DEVICE_LIST_JSON):
        sys.exit()
  
    # get the list 
    with open(CI_DEVICE_LIST_JSON) as device_list_file: 
        device_list_json_obj = json.load(device_list_file)
    device_list = device_list_json_obj["deviceList"]
    for i in range(len(device_list)):
        # print(device_list[i])
        config_file_name = device_list[i] + ".json"
        config_path = os.sep.join([CONFIG_DIR, config_file_name])
        if not os.path.exists(config_path):
            print("Can not find %s for device %s!" % (config_path, device_list[i]))
            continue
        # update the software update time 
        #  "softwareUpdate" : {
        #     "downloadFile" : "downloadFile",
        #     "enable" : "yes",
        #     "forceUpdate" : "false",
        #     "getUpdateConfig" : "getUpdateConfig?config=CI-update-moto-fusion-sensor.json",
        #     "updateTime" : "4:00",
        #     "updateURL" : "https://phone:11222011@software.baysensors.com"
        #   },
        #   "FusionAdmin" : {
        #     "softwareUpdate" : {
        #       "downloadFile" : "downloadFile",
        #       "enable" : "yes",
        #       "forceUpdate" : "false",
        #       "getUpdateConfig" : "getUpdateConfig?config=CI-update-moto-fusion-admin.json",
        #       "updateTime" : "4:34",
        #       "updateURL" : "https://phone:11222011@software.baysensors.com"
        #     }
        #   },
        with open(config_path) as config_path_file: 
            config_json_obj = json.load(config_path_file)
        # for fusion-sensor
        softwareUpdate_node = config_json_obj["softwareUpdate"]
        softwareUpdate_node["enable"] = "yes"
        softwareUpdate_node["forceUpdate"] = "false"
        softwareUpdate_node["getUpdateConfig"] = "getUpdateConfig?config=CI-update-moto-fusion-sensor.json"
        # set target update time
        update_time = int(time.time()) + (15 * 60)
        day_second = update_time % (24 * 3600)
        hour = day_second / 3600
        minute = (day_second % 3600) / 60
        softwareUpdate_node["updateTime"] = "%d:%d" % (hour, minute)
        softwareUpdate_node["updateURL"] = "https://phone:11222011@software.baysensors.com"
        # for fusion admin
        fusion_admin_node = config_json_obj["FusionAdmin"]
        softwareUpdate_node = fusion_admin_node["softwareUpdate"]
        softwareUpdate_node["enable"] = "yes"
        softwareUpdate_node["forceUpdate"] = "false"
        softwareUpdate_node["getUpdateConfig"] = "getUpdateConfig?config=CI-update-moto-fusion-admin.json"
        # set target update time
        update_time = int(time.time()) + (30 * 60)
        day_second = update_time % (24 * 3600)
        hour = day_second / 3600
        minute = (day_second % 3600) / 60
        softwareUpdate_node["updateTime"] = "%d:%d" % (hour, minute)
        softwareUpdate_node["updateURL"] = "https://phone:11222011@software.baysensors.com"
        # update to file
        # save modified json file
        with open(config_path, "w") as config_file:
            json.dump(config_json_obj, config_file, sort_keys=True, indent=4)


if __name__ == '__main__':
    apk_dir = "moto-fusion-sensor"
    # get update type
    parser = OptionParser()
    parser.add_option("-t", "--type", help="Upgrade type, valid values are CI, office, local, others, test")
    (options, args) = parser.parse_args()
    upgrade_type = options.type
    if upgrade_type not in ['CI', 'office', 'local', 'others', 'test']:
        print >> sys.stdout, "Usage:\npython %s --type CI|office|local|others|test\n" % sys.argv[0]
        sys.exit(1)

    # read constants  from json file
    if upgrade_type == 'CI':
        need_constants = ['ROOT_DIR', 'APK_INFO_FILE', 'APK_DIR', 'CI_DEVICE_LIST_JSON', 'CONFIG_DIR', 'SW_UPDATE_DICT']
    else:
    #elif upgrade_type == 'office':
        need_constants = ['ROOT_DIR', 'APK_INFO_FILE', 'APK_DIR', 'SW_UPDATE_DICT']
    #else:
    #    need_constants = []
    #    pass
    if upgrade_type == 'others':
      constants_json_file = os.sep.join([apk_dir, "upgrade_constants.json"])
    else:
      constants_json_file = os.sep.join([apk_dir, upgrade_type, "upgrade_constants.json"])
    if not os.path.isfile(constants_json_file):
        print >> sys.stdout, "constants json file not found: %s" % constants_json_file
        sys.exit(1)

    with open(constants_json_file) as constants_file: 
        constants_json_obj = json.load(constants_file)
    for constant in need_constants:
        if not constants_json_obj.has_key(constant):
            print >> sys.stdout, "constants json file '%s' lost config: %s" % (constants_json_file, constant)
            sys.exit(1)

    # update
    common_upgrade(constants_json_obj)
    if upgrade_type == 'CI':
        ci_extra_upgrade(constants_json_obj)





    # end
