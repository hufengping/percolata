#!/usr/bin/env python

import os
import sys

# software enum
SW_FS = "-fs"
SW_FA = "-fa"
SW_KEY_DICT = {SW_FS : "softwareUpdate.enable",
               SW_FA: "FusionAdmin.softwareUpdate.enable"}

# allow option enum
ALLOW_TRUE = "-t"
ALLOW_FALSE = "-f"
ALLOW_OPTION_DICT = {ALLOW_TRUE : "true",
                     ALLOW_FALSE: "false"}

def update_config(sw_option, allow_option, id_list):
    config_file_dir = "/data/config/"
    edit_cmd = "/data/software/batch_edit_json.py -u "
    key_value = " %s:%s" % (SW_KEY_DICT[sw_option], ALLOW_OPTION_DICT[allow_option])
     
    for placement_id in id_list:
        config_file = config_file_dir + placement_id + ".json"
        if os.path.isfile(config_file):
            update_cmd = edit_cmd + config_file + key_value
            os.system(update_cmd)
            print("Config file update success: ", 
                  config_file, SW_KEY_DICT[sw_option], ALLOW_OPTION_DICT[allow_option])
        else:
           print("File not found: ", config_file)

if __name__ == "__main__":  
    usage_str = """
    Usage:
    allow_software_update.py {SOFTWARE_OPTION} {ALLOW} {[ID1,ID2,ID3,...]}"
        {SOFTWARE_OPTION}:
            -fs:    update fusion sensor config
            -fa:    update fusion admin config
        {ALLOW}:
            -t:     set softwareUpdate.enable "true". allow it upgrade
            -f      set softwareUpdate.enable "false". not allow it upgrade  
        {[ID1,ID2,ID3,...]}:
            placement id list, separate by "," and wrap by "[]"
    """
    
    # arguments count have to greater than 4
    if (len(sys.argv) < 4 
        or sys.argv[1] not in [SW_FS, SW_FA]
        or sys.argv[2] not in [ALLOW_TRUE, ALLOW_FALSE]):
                
        print(usage_str)
        sys.exit() 
    
    # argument have to match the format [ID1,ID2,ID3,...]     
    if sys.argv[3].startswith("[") and sys.argv[3].endswith("]"):
        id_list = sys.argv[3].lstrip("[").rstrip("]").split(",")
    else:
        print(usage_str)
        sys.exit()
        
    sw_option = sys.argv[1]
    allow_option = sys.argv[2]
            
    update_config(sw_option, allow_option, id_list) 
