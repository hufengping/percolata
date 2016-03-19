import os
import json
import hashlib
import time
import inspect
import sys
import shutil
import requests

def generateMd5(content, type="hex"):
    """
    Args:
        content: content to be added md5
    Return:
        md5 string
    """
    m = hashlib.md5()
    m.update(content)
    if type == 'hex':
        return m.hexdigest()
    else:
        return m.digest()
args = sys.argv
print args, len(args)
if len(args) != 4:
    print "Usage: python upload_config.py config_dir end_point environment\n end_point: new_config/modify_config\nenvironment: ci/production"
    sys.exit()
script_name, config_dir, end_point, environment = args

if not os.path.isdir(config_dir):
    print "No such directory '%s'" % config_dir




if environment == 'ci':
    ip = 'https://130.211.149.32'
elif environment == 'production':
    ip = 'https://config.percolata.com'
else:
    ip="http://localhost:5000"
no_files = []
ok_files = []
failed_files = []

for fl in os.listdir(config_dir):
    placement_name = os.path.splitext(fl)[0]
    file_path = os.path.join(config_dir, fl)
    with open(file_path, 'rb') as f:
        c = f.read()
    md5 = generateMd5(c)
    rv = requests.post("%s/modify_config" % ip, auth=('phone', '11222011'),
                       headers={'HOST': 'config.percolata.com'},
                       data={
                           'placement_name': placement_name,
                           'file_name': placement_name+'.json',

                           'md5': md5},
                       files={'file': open(file_path, 'rb')},
                       verify=False)
    time.sleep(1)
    print rv.content
    if not rv.status_code==200:
        failed_files.append(placement_name)
    # cmd = "curl  -k  --header 'HOST: config.percolata.com' --form placement_name=%s --form file_name=%s.json --form file=@%s --form md5=%s https://phone:11222011@%s/%s" % \
    #       (placement_name, placement_name, file_path, md5, ip, end_point)
    # print cmd

    # os.system(cmd)
    ok_files.append(placement_name)
    # shutil.copy(file_path, ok_dir + placement_name + '.json')

print " ============= ok ==============="
for i in ok_files:
    print i

print " ============= process failed ========="
for i in failed_files:
    print i

