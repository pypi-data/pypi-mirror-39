# -*- coding: utf-8 -*-
__all__ = ['win_set_time_by_now']


def win_set_time_by_now(days=0):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

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
    win_set_time_by_now(3)


