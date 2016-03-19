import os
import sys
import boto
conn = boto.connect_gs()
def Usage():
    print "python download_gs_dir.py <bucket name> <google storage path> <save dir>\n\nExample: python download_gs_dir.py percolata logdump/ /tmp/save/"
    sys.exit()
try:
    script, bucket_name, gs_dir, save_dir = sys.argv
except:
    Usage()

bucket = conn.get_bucket(bucket_name)
print bucket
for key in bucket.list(gs_dir):
    print key, key.name
    save_path = os.path.join(save_dir, key.name)
    file_dir = os.path.split(save_path)[0]
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    try:
        res = key.get_contents_to_filename(save_path)
        print "download ok: %s" % key.name
    except Exception as e:
        print e
        print (key.name+":"+"FAILED")