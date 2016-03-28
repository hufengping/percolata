import re,os

str = "/home/fengpinghu/temp/logdump/2016-02-16/8600067/FusionSensor.apk"

print re.findall(r'^/',str)

#print str.split('/temp/')[1]
#print os.path.split(str)[0]
