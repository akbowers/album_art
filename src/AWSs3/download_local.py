'''
    Downloads files off of s3 bucket and saves locally to hard drive.
'''

import os
import boto3
from collections import defaultdict

def get_files_from_bucket(limit, bucket_name, list_to_search):
    s3 = boto3.client('s3')
    bucket = boto3.resource('s3').Bucket(bucket_name)
    bo = bucket.objects
    genre_keys = defaultdict(list)
    for b in bo.iterator():
        genre = b.key.split('/')[0]
        if genre in list_to_search:
            if len(genre_keys[genre]) < limit:
                genre_keys[genre].append(b.key)

    return genre_keys

def make_subdirs(genre_keys, destination):
    for genre in genre_keys:
        new_path = os.path.join(destination, genre)
        if not os.path.exists(new_path):
            os.mkdir(new_path)


def save_to_drive(genre_keys, destination, bucket_name):
    s3 = boto3.client('s3')
    filenames = []
    for genre in genre_keys:
        keys = genre_keys[genre]
        for key in keys:
            dest_path = os.path.join(destination, key)
            if not os.path.exists(dest_path):
                filenames.append(dest_path)
                print 'Saving {}'.format(dest_path)
                s3.download_file(bucket_name, key, dest_path)
