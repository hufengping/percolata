"""
google storage manger
usage:
from download_gsDir_to_local import GSManager
BUCKET_NAME = 'percolata-test'
REMOTE_DIR = 'data/combined/zone_count/'
gs_worker = GSManager(BUCKET_NAME)
LOCAL_WORK_DIR = './tmp/'
gs_worker.download_dir_to_local(remote_dir, LOCAL_WORK_DIR)

"""
import os
import sys
import boto

# from boto.gs.connection import GSConnection
from boto.gs.key import Key


class GSManager(object):

    def __init__(self, bucket_name):
        self.conn = boto.connect_gs()
        self.bucket = self._bucket(bucket_name)

    def _bucket(self, bucket_name):
        """
        generate a gs bucket obj with bucket name.
        if bucket is not exists, create one.

        Return:
            bucket obj
        """
        # Get the bucket object. If it does not exist, create one.
        bucket = self.conn.lookup(bucket_name)
        if bucket is None:
            bucket = self.conn.create_bucket(bucket_name)
        return bucket

    def upload_to_GS(self, local_file_path, gs_file_path, replace=True):
        """
        Args:
            local_file_path: local file path which user want to upload to google storage
            gs_file_path: file path that stored on google storage
        Return:
            upload result
        """
        gs_file_path = self._normpath(gs_file_path)
        obj = Key(self.bucket)
        obj.key = gs_file_path
        obj.set_contents_from_filename(local_file_path, replace=replace)
        return True

    def get_content_from_file(self, gs_file_path):
        """
        get the content of file on google storage
        Args:
            gs_file_path: file path on google storage
        Return:
            content string
        """
        gs_file_path = self._normpath(gs_file_path)
        gs_key = self.bucket.get_key(gs_file_path)
        if not gs_key:
            return False
        else:
            return gs_key.get_contents_as_string()

    def check_if_exists(self, gs_file_path, return_obj=False):
        """
        check if gs exists file
        Args:
            gs_file_path: file path on gs
        Return:
            exists: True
            not exists: False
        """
        gs_file_path = self._normpath(gs_file_path)
        gs_key = self.bucket.get_key(gs_file_path)
        if gs_key:
            return True
        else:
            return False

    def download_to_local(self, gs_file_path, local_file_path):
        """
        download gs file to local
        Args:
            local_file_path: local path to store file
            gs_file_path: gs file path to be downloaded
        Return:
            download ok: True
            download failed: error information
        """
        gs_file_path = self._normpath(gs_file_path)
        # make local diretory
        local_file_dir = os.path.split(local_file_path)[0]
        if not os.path.isdir(local_file_dir):
            os.makedirs(local_file_dir)
        # check if gs exists file
        gs_key = self.bucket.get_key(gs_file_path)
        if not gs_key:
            return "No such file on gs: %s" % gs_file_path

        # get file from gs
        if not os.path.exists(local_file_path):
            tmp_file = file(local_file_path, 'wb')
            tmp_file.close()
        gs_key.get_contents_to_filename(local_file_path)
        return True

    def download_dir_to_local(self, gs_file_dir, local_dir):
        """
        download gs file under gs_file_dir to local_dir
        Args:
            local_file_dir: local diretory to store file
            gs_file_dir: gs file diretory to be downloaded
        """
        file_list = []
        for item in self.bucket.list(gs_file_dir, "/"):
            file_list.append(item.name)
        for item in file_list:
            tmp_index = item.rfind('/')
            print item
            local_file_path = local_dir + item[tmp_index + 1:]
            print local_file_path
            self.download_to_local(item, local_file_path)

    def delete_gs_resource(self, resource_path):
        """
        delete file or floder on gs
        Args:
            resource_path: file or floder path on gs
        """
        gs_file_path = self._normpath(resource_path)
        gs_key = self.bucket.get_key(gs_file_path)
        if gs_key:
            gs_key.delete()

    def _normpath(self, path):
        """
        Args:
            path: transfer the input path to normal path to gs path
        Return:
            normal path
        """
        gs_path = os.path.normpath(path)
        if gs_path.startswith('/'):
            gs_path = gs_path[1:]
        return gs_path

    def close(self):
        """
        close connection
        """
        self.conn.close()

if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) != 4:
        print "Usage: python download_gsDir_to_local.py bucket_name gs_dir local_dir"
    script, bucket_name, gs_dir, local_dir = args
    local_dir = local_dir+'/'
    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)
    gs_manager = GSManager(bucket_name)
    print "start to download %s to %s" % (gs_dir, local_dir)
    gs_manager.download_dir_to_local(gs_dir, local_dir)
    print "download ok"
