from .date_util import DateUtil

class Decorator(object):

    @staticmethod
    def timer_handler(func):
        def f(*args, **kwargs):
            print('job start time:{0}'.format(DateUtil.getLocalTodayDateString(True, True)))
            rv = func(*args, **kwargs)
            print('job end time:{0}'.format(DateUtil.getLocalTodayDateString(True, True)))
            return rv
        return f

