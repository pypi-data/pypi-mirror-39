# -- coding: utf-8 --

from GlodonLibrary.keywords import *
from .version import VERSION

class GlodonLibrary(
    PublicFunction,
    Control,
    HttpReq,
    FileRead,
    BaseFunc,
    RedisFunc,
    run_program,
    GetBoxParams,
    restart_service,
    start_service,
    win_set_time_by_now
):

    """自定义的方法库"""
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def win_set_time_by_now(self, days=0):
        import datetime
        from datetime import timedelta
        import win32api
        global now
        now = datetime.datetime.now()
        if isinstance(days, int) and days > 0:
            new_time = now + timedelta(days=days)
        elif isinstance(days, int) and days < 0:
            new_time = now - timedelta(days=days)
        else:
            new_time = now
        new_time_tuple = new_time.timetuple()[:2] + (new_time.isocalendar()[2],) + new_time.timetuple()[2:6] + (0,)
        print(new_time_tuple)
        win32api.SetSystemTime(
            new_time_tuple[0],
            new_time_tuple[1],
            new_time_tuple[2],
            new_time_tuple[3],
            new_time_tuple[4],
            new_time_tuple[5],
            new_time_tuple[6],
            new_time_tuple[7]
        )
        
        
if __name__ == '__main__':
    pass