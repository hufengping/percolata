import os
import sys
import json
import traceback
import shutil
def Usage():
    print "Usage: python modify_config_files.py modify_config source_device_config_files_path store_result_path\nEg. python modify_config_files.py config.conf device_config result_config"
    sys.exit()

args = sys.argv
print args

try:
    config, config_dir, result_dir = sys.argv[1:]
    print config, config_dir, result_dir
except:
    Usage()
if not os.path.isfile(config):
    print "Can't find config file: %s" % config
    Usage()
if not os.path.isdir(config_dir):
    print "Can't find config dir: %s" % config_dir
    Usage()
if os.path.isdir(result_dir):
    shutil.rmtree(result_dir)
os.makedirs(result_dir)

with open(config, 'rb') as f:
    config = f.readlines()

delete_keys = []
modify_kv = {}
extra = False
succ_devices = []
error_devices_info = {}
for line in config:
    line = line.strip()
    if line == "":
        continue
    if not (line.startswith('delete:') or line.startswith('modify:') or line.startswith('#') or line.startswith("extra")):
        print "invalid config line: '%s'" % line, config.index(line)
        sys.exit()
    if line.startswith('delete:'):
        delete_keys.append(line.split(':')[1])
    if line.startswith('modify'):
        k, v = line.split(':', 1)[1].split('=', 1)
        modify_kv[k] = v
    if line.startswith('extra'):
        extra = True

for d_config_file in os.listdir(config_dir):
    f_path = os.path.join(config_dir, d_config_file)
    try:
        with open(f_path, 'rb') as f:
            d_config = f.read()
            d_config_dict = json.loads(d_config)

        if extra:
            s_keys = d_config_dict['softwareUpdate'].keys()
            if "getUpdateConfig" in s_keys:
                d_config_dict['softwareUpdate']['type'] = "production"
            elif "getLocalUpdateConfig" in s_keys:
                d_config_dict['softwareUpdate']['type'] = "local"
            elif "getOfficeUpdateConfig" in s_keys:
                d_config_dict['softwareUpdate']['type'] = "office"
            else:
                error_devices_info[d_config_file] = "softwareUpdate has invalid update type %s" % s_keys
                continue
        for d_k in delete_keys:
            sub_keys = d_k.split('/')
            sub_dict = d_config_dict
            for i in range(len(sub_keys)-1):
                sub_dict = sub_dict[sub_keys[i]]
            sub_dict.pop(sub_keys[-1])
        for m_k in modify_kv:
            sub_keys = m_k.split('/')
            sub_dict = d_config_dict
            for i in range(len(sub_keys)-1):
                sub_dict = sub_dict[sub_keys[i]]
            sub_dict[sub_keys[-1]] = modify_kv[m_k]

        with open(os.path.join(result_dir, d_config_file), 'wb') as f:
            f.write(json.dumps(d_config_dict, indent=4, separators=[',', ':'], sort_keys=True))
        succ_devices.append(d_config_file)

    except Exception as e:
        print traceback.format_exc()
        error_devices_info[d_config_file] = "failed to process %s, error is: %s" % (d_config_file, str(e))

print "========== process result ==========="
print "successful:"
for d in succ_devices:
    print d
print "-" * 20
print "failed config\tfailed reason"
for d in error_devices_info:
    print d, "\t", error_devices_info[d]








