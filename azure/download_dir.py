import os
from backend_common.storage import storage_manager
import sys
import shutil

import sys
#	need install boto and azure
args = sys.argv
try:
    bucket_name, directory, save_dir = args[1:]
except Exception as e:
    print "Usage: python download_dir.py <bucket_name> <directory> <save_dir>\n\neg. python download_dir.py percolata-data software/fixed software"
    sys.exit()

save_dir = os.path.expanduser(save_dir)
storage_type = 1

if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

storage_path = storage_manager.generate_storage_path(storage_type, bucket_name, directory)
print storage_path
storage_manager.download_dir_to_local(storage_path, save_dir)

print "download %s to %s ok" % (directory, save_dir)

