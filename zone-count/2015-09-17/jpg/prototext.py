#!/usr/bin/env python

from protobuf_messages.zone_count_data_pb2 import Video
import argparse
import os
import filesCount as fc

v = Video()
filelist = fc.GetFileList(os.getcwd(),".zoneCountproto")
print "----------------------------------"
print "all files: ", filelist
print "=" * 30
for files in filelist:
	print files, '\n'
	f=file(files+".txt","w+")
	with open(files) as fin:
		msg = fin.read()
	       	v.ParseFromString(msg)
	       	print str(v)
	       	f.write(str(v))
		#print type(msg)
