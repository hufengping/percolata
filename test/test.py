#!/usr/bin/env python
'''
@author: fengpinghu
'''
#coding=utf-8

from backend_common.storage import storage_manager

import sys,os


args = sys.argv
try:
    bucket_name, fpath, save_path = args[1:]
except Exception as e:
    print "Usage: python download_dir.py <storage_type> <bucket_name> <fpath> <save_path>\n\neg. python download_dir.py percolata-data software/fixed/1.json software"
    sys.exit()

save_path = os.path.expanduser(save_path)
storage_type = 2


storage_path = storage_manager.generate_storage_path(storage_type, bucket_name, fpath)

storage_manager.download_to_local_path(storage_path, save_path)

print "download %s to %s ok" % (fpath, save_path)
