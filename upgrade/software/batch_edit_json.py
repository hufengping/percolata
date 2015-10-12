#!/usr/bin/env python

import json
import os
import sys
from _ast import Str


# constants
KEY_VALUE_SEP = ":"
KEY_SEP = "."

# action enum
ACTION_FIND = "-f"
ACTION_INSERT = "-i"
ACTION_DELETE = "-d"
ACTION_UPDATE = "-u"

JSON_FILE_DIR = "/data/config/"
JSON_FILE_SUFFIX = ".json"


def find_deepest_json_obj(json_obj, key_list, action):
    """Recursive function, find the deepest item contain the key list
    
    """
    # if json_obj does not contain the key, do nothing
    if key_list[0] not in json_obj:
        if action == ACTION_INSERT:
            json_obj.setdefault(key_list[0], {})
        else:
            return None
    
    if len(key_list) > 1:
        return find_deepest_json_obj(json_obj[key_list[0]], key_list[1:], action)
    else:
        print("Find the deepest item, ", key_list[0], json_obj[key_list[0]])
        return json_obj;
                    
def update_json_value(json_obj, key, value):       
    # update json value
    json_obj[key] = value
    print("Update json value success: ", key, json_obj[key])
    
    return json_obj

def insert_json_value(json_obj, key, value):
    # insert json value
    json_obj[key] = value
    print("Insert json value success: ", key, json_obj[key])
    return json_obj  
        
def delete_json_value(json_obj, key):
    print("Delete json value success: ", key, json_obj[key])
    # delete json value  
    json_obj.pop(key)
    return json_obj
        
def edit_json_file(json_obj, key_value_list, action):
    for key_value in key_value_list:
        # parse combined_key and value
        if KEY_VALUE_SEP in key_value:
            combined_key, update_value = key_value.split(KEY_VALUE_SEP)
        else:
            combined_key = key_value
            update_value = ""            
        if combined_key == "":
            continue
        
        # parse key list
        if KEY_SEP in combined_key:
            key_list = combined_key.split(KEY_SEP)
        else:
            key_list = [combined_key]
            
        action_obj = find_deepest_json_obj(json_obj, key_list, action)
        if action_obj == None:
            print("The deepest json object is null.")
        else:
            # execute action to the json object
            if action == ACTION_FIND:
                # no need more operation
                pass
            elif action == ACTION_INSERT:
                insert_json_value(action_obj, key_list[-1], update_value)
            elif action == ACTION_DELETE:
                delete_json_value(action_obj, key_list[-1])
            elif action == ACTION_UPDATE:
                update_json_value(action_obj, key_list[-1], update_value)
                
    return json_obj
    
def load_json_file(json_file):
    if os.path.exists(json_file):
        # load json file  
        with open(json_file) as file_obj:
            json_obj = json.load(file_obj)
            print("load json file success: ", json_file)
    else:
        json_obj = None
        print("load json file fail: ", json_file)
        
    return json_obj

def save_json_file(json_obj, json_file):
    with open(json_file, "w") as file_obj:
        json.dump(json_obj, file_obj, sort_keys=True, indent=4)
        
# test script
if __name__ == "__main__":
    usage_str = """
    Usage:
    batch_edit_json.py {ACTION} {DIR OR File PATH OR [ID_LIST] OR ID_FILE} 
                            {KEY1.KEY2.KEY:VALUE} ...
        {ACTION}:
            -f:        find the item according certain key
            -i:        insert a new item to json file
            -d:        delete the item according certain key
            -u:        update the item according certain key
        {DIR OR File PATH OR [ID_LIST]}:
            dir:       edit all json file in this directory
            file:      only edit the json file, the suffix is json
            [id_list]: [placement_id1,placement_id2,placement_id3...]
            id_file:   input file contians placement ids, one row only has one id
        {KEY1.KEY2.KEY:VALUE}:
            KEY:        OuterKey.InnerKey.Key (Maybe nest many layers)
            ":":        Have to contain the separator even if the value is ""
            VALUE:      Maybe is ""
            this argument can have more than one, and all will be update                
    """
    
    # arguments count have to greater than 4
    if (len(sys.argv) < 4 or sys.argv[1] not in 
        [ACTION_FIND, ACTION_INSERT, ACTION_DELETE, ACTION_UPDATE]):
        
        print(usage_str)
        sys.exit()        
    
    
    # record arguments            
    action = sys.argv[1]
    json_path = sys.argv[2]
    key_value_list = sys.argv[3:]
   
    # handle json file path    
    file_list = list()        
    if os.path.isdir(json_path):
        # only handle json file
        for file in os.listdir(json_path):
            if isinstance(file, str) and file.endswith(JSON_FILE_SUFFIX):
                file_list.append(file)            
    elif os.path.isfile(json_path):
        if json_path.endswith(JSON_FILE_SUFFIX):
            # need edited json file
            json_path, file_name = os.path.split(json_path)       
            file_list.append(file_name)
        else:
            # id input file
            with open(json_path) as input_file:
                for line in input_file.readlines():
                    line = line.strip() # remove empty char
                    if not len(line) or line.startswith('#'):
                        # skip the empty line or comment line  
                        continue
                    file_list.append(line + JSON_FILE_SUFFIX  )  
            json_path = JSON_FILE_DIR
    elif json_path.startswith("[") and json_path.endswith("]"):
        id_list = json_path.lstrip("[").rstrip("]").split(",")
        # add json file suffix to every id
        for id in id_list:
            file_list.append(id + JSON_FILE_SUFFIX)                      
        json_path = JSON_FILE_DIR
    else:
        print("Directory or file path does not exist: ", json_path)
        sys.exit()
    
    # change to work space
    if os.path.isdir(json_path):
        os.chdir(json_path)        
    #print("Current path: ", os.getcwd())
        
    for file_name in file_list:
        # TODO: Change it to match pattern
        json_obj = load_json_file(file_name)
        if json_obj == None:
            continue
        
        edit_json_file(json_obj, key_value_list, action)
            
        save_json_file(json_obj, file_name)



    
