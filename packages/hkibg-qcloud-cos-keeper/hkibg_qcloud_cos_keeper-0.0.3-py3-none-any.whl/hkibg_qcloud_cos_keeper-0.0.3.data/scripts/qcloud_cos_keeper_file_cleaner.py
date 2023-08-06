#!python
import os
import sys
import io
import time
import hkibg_qcloud_cos_keeper
from hkibg_qcloud_cos_keeper import *
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

@Decorator.timer_handler
def run():

    args = ArgsUtil.loadArgumentParseModule([
        {'name':'filepath', 'default':'/home/src/archive/', 'help':'archive file path', 'required':False},
        {'name':'fileage', 'default':'monthly', 'help':'file age', 'required':False, 'choices':['day', 'week', 'month']}
    ])

    if args.fileage == 'day':
        age_bound = time.time() - 1 * 86400   
    elif args.fileage == 'week':
        age_bound = time.time() - 7 * 86400   
    else:
        age_bound = time.time() - 30 * 86400   

    print('age bound:{0}'.format(age_bound))

    for root, dirs, files in os.walk(args.filepath, topdown=False):
        if files:
            for item in files:
                file_ts = os.stat(Util.singleRightSlash(root) + item).st_mtime
                if file_ts < age_bound:
                    print('Deleting older file:{0}, with ts:{1}'.format(item, file_ts))
                    os.unlink(Util.singleRightSlash(root) + item)
                else:
                    print('Ignoring file:{0}, with ts:{1}'.format(item, file_ts))

if __name__ == "__main__":
    run()

