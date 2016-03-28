import os
from backend_common.storage import storage_manager
import sys
import shutil

import sys
#	need install boto and azure
args = sys.argv
try:
    bucket_name, directory, local_file = args[1:]
except Exception as e:
    print "Usage: python upload_file.py <bucket_name> <directory> <local_file>\n\neg. python upload_file.py percolata-data software/fixed ./test/test.json"
    sys.exit()

local_file = os.path.expanduser(local_file)
storage_type = 1

if os.path.exists(local_file):
    fp = open(local_file)
else:
    print "file not found: %s" % local_file

storage_path = storage_manager.generate_storage_path(storage_type, bucket_name, directory)
print storage_path
storage_manager.upload_to_container_from_file(storage_path, fp)

print "upload %s to %s ok" % (local_file, directory)
