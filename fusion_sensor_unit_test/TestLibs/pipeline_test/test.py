#!/usr/bin/env python
import sys

sys.path.append("./protobuf_messages")
from loi_pb2 import LOIForegroundBlobData
MSG = LOIForegroundBlobData()

with open("templates/loi_template_01.blobproto",'rb') as infile:
    MSG.ParseFromString(infile.read())
    print MSG
    MSG.startTimestamp = 1
    MSG.endTimestamp =2
    with open("test.out",'wb') as outfile:
        outfile.write(MSG.SerializeToString())
        outfile.close()


