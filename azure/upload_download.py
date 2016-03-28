import os
from backend_common.storage import storage_manager


def upload_file(bucket_name, directory, local_file):

    #Usage: python upload_file.py <bucket_name> <directory> <local_file>\n\neg. python upload_file.py percolata-data software/fixed ./test/test.json

    local_file = os.path.expanduser(local_file)
    storage_type = 2

    if os.path.exists(local_file):
        fp = open(local_file)
    else:
        print "file not found: %s" % local_file

    storage_path = storage_manager.generate_storage_path(storage_type, bucket_name, directory)
    print storage_path
    storage_manager.upload_to_container_from_file(storage_path, fp)

    print "upload %s to %s ok" % (local_file, directory)


def download_dir(bucket_name, directory, save_dir):

    # Usage: python download_dir.py <bucket_name> <directory> <save_dir>\n\neg. python download_dir.py percolata-data software/fixed software

    save_dir = os.path.expanduser(save_dir)
    storage_type = 2

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    storage_path = storage_manager.generate_storage_path(storage_type, bucket_name, directory)
    print storage_path
    storage_manager.download_dir_to_local(storage_path, save_dir)

    print "download %s to %s ok" % (directory, save_dir)
