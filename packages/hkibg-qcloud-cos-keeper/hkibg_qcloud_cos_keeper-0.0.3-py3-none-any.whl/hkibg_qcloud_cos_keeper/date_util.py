import time
from datetime import date, timedelta, datetime
import pytz, tzlocal

#assume the container image is +00:00
#and timezone of the container image is Asia/Hong Kong
#conversion between date string and timestamp
class DateUtil(object):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    fmt_with_time = "%Y-%m-%d %H:%M:%S"
    fmt_no_time = "%Y-%m-%d"
    local_timezone = tzlocal.get_localzone()
    utc_timezone = pytz.utc

    #convert timestamp to local date string
    @staticmethod
    def timestampToLocalDateString(timestamp):
        utc_date_object = datetime.fromtimestamp(timestamp)
        return DateUtil.getLocalDateString(utc_date_object, True, True)
    
    @staticmethod
    def timestampToDateObject(timestamp):
        return datetime.fromtimestamp(timestamp)

    #convert date object to timestamp
    @staticmethod
    def localDateStringToTimestamp(date_string):
        local_timezone = tzlocal.get_localzone()

        #create naive datetime object, DT object with no timezone info
        if len(date_string) > 10:
            naive_dt_object = datetime.strptime(date_string, DateUtil.fmt_with_time)
        else:
            naive_dt_object = datetime.strptime(date_string, DateUtil.fmt_no_time)
        
        #add local timezone info buy localize method
        local_dt_object = local_timezone.localize(naive_dt_object)
        #convert to utc before making timestamp
        utc_dt_object = local_dt_object.astimezone(pytz.utc)
        #print(local_dt_object.strftime(DateUtil.fmt))
        #print(utc_dt_object.strftime(DateUtil.fmt))
        return float(time.mktime(utc_dt_object.timetuple()))

    @staticmethod
    def getLocalDateByDateFormat(date_object, date_format):
        local_date = DateUtil.localizeDateObject(date_object)
        return local_date.strftime(date_format)

    @staticmethod
    def getLocalTodayByDateFormat(date_format):
        utc_today = datetime.today()
        local_today = DateUtil.localizeDateObject(utc_today)
        return local_today.strftime(date_format)

    @staticmethod
    def getLocalTodayDateString(withTime=False, currentTime=False):
        utc_today = datetime.today()
        return DateUtil.getLocalDateString(utc_today, withTime, currentTime)

    @staticmethod
    def getLocalYesterdayByDateFormat(date_format):
        utc_yesterday = datetime.today() - timedelta(1)
        local_yesterday = DateUtil.localizeDateObject(utc_yesterday)
        return local_yesterday.strftime(date_format)

    @staticmethod
    def getLocalYesterdayDateString(withTime=False, currentTime=False):
        utc_yesterday = datetime.today() - timedelta(1)
        return DateUtil.getLocalDateString(utc_yesterday, withTime, currentTime)

    @staticmethod
    def getLocalDateString(utc_date_object, withTime=False, currentTime=False):
        local_date_object = DateUtil.localizeDateObject(utc_date_object)
        if withTime:
            if currentTime:
                return local_date_object.strftime(DateUtil.fmt_with_time)
            else:
                return local_date_object.strftime(DateUtil.fmt_no_time) + " 00:00:00"
        else:
            return local_date_object.strftime(DateUtil.fmt_no_time)

    @staticmethod
    def localizeDateObject(date_object):
        #add local timezone info buy localize method
        local_date_object = date_object.astimezone(DateUtil.local_timezone)
        return local_date_object 

