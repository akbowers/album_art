import os
from datetime import datetime
from time import time

def get_filenames_in_tmp(path):
    return os.listdir(path)

def get_path_update_timestamps(path):
    '''
    returns unix timestamp for last time path was modefied. We actually want tstamps
    for EACH file
    '''
    return os.path.getmtime(path)

def get_file_timestamp(filename):
    try:
        mtime = os.path.getmtime(filename)
    except OSError:
        print 'We had an OSError, folks!'
        mtime = 0

    last_modified_date = datetime.fromtimestamp(mtime)
    return mtime

def get_current_timestamp():
    '''
    Just for fun, we convert to humam readable dt. Never actually use this
    '''
    mtime = time()
    current_time = datetime.fromtimestamp(mtime)
    return current_time

def get_file_age(now, creation_time):
    return now - creation_time

if __name__ == '__main__':
    tmp_files = get_filenames_in_tmp('static/tmp/')
    print tmp_files
    print get_path_update_timestamps('static/tmp/')

    now = time()

    for fname in tmp_files:
        f_path = os.path.join('static/tmp', fname)
        print 'file name: {}, timestamp: {}'.format(f_path, get_file_timestamp(f_path))
        creation_time = get_file_timestamp(f_path)
        file_age = get_file_age(now, creation_time)
        print 'file name: {}, file age: {}'.format(f_path, file_age)
        if file_age > 2000: #if it's old enough kill it
            os.remove(f_path)

    print 'The current date and time is {}'.format(get_current_timestamp())
