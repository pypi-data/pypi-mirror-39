#!python
import os
import sys
import io
import hkibg_qcloud_cos_keeper
from hkibg_qcloud_cos_keeper import *
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#compute the cos file path
def get_cos_file_path(module_folder, host_folder, main_folder, date_folder, ts=0):
    #resolve hostname folder
    if module_folder is False:
        module_folder = ''
    else:
        module_folder = Util.singleRightSlash(module_folder)

    if main_folder is False:
        main_folder = ''
    else:
        main_folder = Util.singleRightSlash(main_folder)

    if date_folder == 'yearly':
        date_format = '%Y'
    elif date_folder == 'monthly':
        date_format = '%Y%m'
    elif date_folder == 'daily':
        date_format = '%Y%m%d'
    else:
        date_format = ''

    if not date_format:
        sub_folder == ''
    else:
        if ts == -1:
            sub_folder = Util.singleRightSlash(DateUtil.getLocalYesterdayByDateFormat(date_format))
        elif ts == 0:
            sub_folder = Util.singleRightSlash(DateUtil.getLocalTodayByDateFormat(date_format))
        else:
            sub_folder = Util.singleRightSlash(DateUtil.getLocalDateByDateFormat(DateUtil.timestampToDateObject(ts), date_format))

    return module_folder + host_folder + main_folder + sub_folder

@Decorator.timer_handler
def run():
    args = ArgsUtil.loadArgumentParseModule([
            {'name':'filepath', 'default':'/home/src/archive/', 'help':'source file path. Default: /home/src/archive/', 'required':False},
            {'name':'hostname', 'default':os.getenv('HOSTNAME', ''), 'help':'include hostname in cos file path. If it is null, skipped this part', 'required':False},
            {'name':'mainfolder', 'default':'default', 'help':'cos main folder, after project and hostname', 'required':False},
            {'name':'datefolder', 'default':'monthly', 'help':'cos date folder, after project, hostname and main folder, arranging files by date folder. Default: monthly', 'required':False, 'choices':['yearly', 'monthly', 'daily', 'none']},
            {'name':'yesterday', 'default':False, 'help':'use yesterday date for date folder. Default: False.', 'required':False},
            {'name':'qcloud_appid', 'default':os.getenv('QCLOUD_APPID', ''), 'help':'qcloud app id', 'required':False},
            {'name':'qcloud_secret_id', 'default':os.getenv('QCLOUD_SECRET_ID', ''), 'help':'qcloud secret id', 'required':False},
            {'name':'qcloud_secret_key', 'default':os.getenv('QCLOUD_SECRET_KEY', ''), 'help':'qcloud secret key', 'required':False},
            {'name':'qcloud_cos_region', 'default':os.getenv('QCLOUD_COS_REGION', ''), 'help':'qcloud cos region', 'required':False},
            {'name':'qcloud_cos_scheme', 'default':os.getenv('QCLOUD_COS_SCHEME', ''), 'help':'qcloud cos region', 'required':False},
            {'name':'qcloud_cos_bucket', 'default':os.getenv('QCLOUD_COS_BUCKET', ''), 'help':'qcloud cos bucket', 'required':False},
            {'name':'qcloud_cos_folder', 'default':os.getenv('QCLOUD_COS_FOLDER', ''), 'help':'qcloud cos folder', 'required':False}
    ])

    if args.hostname:
        host_folder = Util.singleRightSlash(args.hostname)
    else:
        host_folder = ''

    cos_object = CosUtil(args.qcloud_appid, args.qcloud_secret_id, args.qcloud_secret_key, '', args.qcloud_cos_region, args.qcloud_cos_scheme)
    bucket = args.qcloud_cos_bucket

    local_file_path = Util.singleRightSlash(args.filepath)

    for root, dirs, files in os.walk(args.filepath, topdown=False):
        if files:
            for filename in files:
                file_ts = os.stat(Util.singleRightSlash(root) + filename).st_mtime
                if args.yesterday is False:
                    cos_file_path = get_cos_file_path(args.qcloud_cos_folder, host_folder, args.mainfolder, args.datefolder, -1)
                else:
                    cos_file_path = get_cos_file_path(args.qcloud_cos_folder, host_folder, args.mainfolder, args.datefolder, file_ts)
                etag = cos_object.putFile(bucket, local_file_path + filename, cos_file_path + filename)
                if etag:
                    print('cos file uploaded. bucket:{0}, local_file_path:{1}, cos_file_path:{2}, file:{3}, etag:{4}'.format(bucket, local_file_path, cos_file_path, filename, etag))

if __name__ == "__main__":
    run()

