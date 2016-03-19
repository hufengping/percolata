#!/usr/bin/env python

import boto
import logging

URL="percolata-test/data/fragment/img/dump/8600066/2015-07-07/8600066_es-2015-07-07-08-27-27_0001.jpg"

logger = logging.getLogger("tmpLogger")
def get_data_from_gs(gs_conn, path):
    """download blob files from GS"""
    bucket_key_name = get_bucket_and_key(path)
    bucket = gs_conn.get_bucket(bucket_key_name[0])
    key = bucket.get_key(bucket_key_name[1])
    try:
        content = key.get_contents_as_string()
        logger.info("test")
        return content
    except Exception as e:
        logger.error('Error in downloading %s from bucket %s' % (key.name, bucket_key_name[0]))
        raise

def get_bucket_and_key(gs_path):
    """get bucket name and key name from
        google storage path
    ARGS: string of google storage path
    RETURNS: a tuple of bucket name and key name
    """
    index = gs_path.find('/')
    bucket_name = gs_path[:index]
    key_name = gs_path[(index + 1):]
    return (bucket_name, key_name)


if __name__ == "__main__":
    gs_conn = boto.connect_gs()
    data = get_data_from_gs(gs_conn, URL)
    with open("img1.jpg","wb") as fp:
        fp.write(data)
        fp.close()
