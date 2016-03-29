import re,os
from upload_download import *
str = "/home/fengpinghu/temp/logdump/2016-02-16/8600067/FusionSensor.apk"

print re.findall(r'^/',str)
print str.split("/", 3)[3]

download_dir("perolata-test", "logdump", "/home/deployer/test/percolata-test")

#print str.split('/temp/')[1]
#print os.path.split(str)[0]
