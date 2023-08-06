#!python
import os
import shutil
import sys
import io
import hkibg_qcloud_cos_keeper
from hkibg_qcloud_cos_keeper import *
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_suffix(freq, match_date=False, ts=0):
    if freq == 'weekly':
        date_format = '%w'
    elif freq == 'monthly':
        date_format = '%d'
    else:
        date_format = '%Y%m%d'
        
    if match_date is False:
        suffix = DateUtil.getLocalTodayByDateFormat(date_format)
    else:
        suffix = DateUtil.getLocalDateByDateFormat(DateUtil.timestampToDateObject(ts), date_format)
    return suffix

@Decorator.timer_handler
def run():
    args = ArgsUtil.loadArgumentParseModule([
        {'name':'freq', 'default':'none', 'help':'choose the extension of rotated filename. If set to weekly, filename will have suffix from 0-6, overwriting itself weekly. Default: none, using YYYYmmdd as suffix.', 'required':False, 'choices':['none','weekly','monthly']},
        {'name':'pattern', 'default':'log', 'help':'Only move file name contains the keyword [pattern]', 'required':False},
        {'name':'use_file_ts', 'default':False, 'help':"If true, the timestamps of the file will be used as the ext of the moved file. If false, the system date will be used as the file extension", 'required':False},
        {'name':'src_path', 'default':'/home/src/log/', 'help':'src file path', 'required':False},
        {'name':'dest_path', 'default':'/home/src/archive/', 'help':'dest file path', 'required':False}#,
    ])

    for root, dirs, files in os.walk(args.src_path, topdown=False):
        local_file_path = Util.singleRightSlash(args.src_path)
        if files:
            for filename in files:
                #allow pattern matching
                if args.pattern in filename:
                    #compute suffix
                    file_ts = os.stat(Util.singleRightSlash(root) + filename).st_mtime
                    suffix = get_suffix(args.freq, args.use_file_ts, file_ts)
                    src_file = Util.singleRightSlash(args.src_path) + filename
                    dst_file = Util.singleRightSlash(args.dest_path) + filename + '.' + suffix
                    shutil.move(src_file, dst_file)
                    print("moving file from {0} to {1}".format(src_file, dst_file))

if __name__ == "__main__":
    run()

