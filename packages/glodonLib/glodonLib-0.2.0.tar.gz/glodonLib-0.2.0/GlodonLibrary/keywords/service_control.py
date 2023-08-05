# coding:utf-8

import time
import datetime
from datetime import timedelta

import win32api
import win32serviceutil



status_code = {

    0: "UNKNOWN",

    1: "STOPPED",

    2: "START_PENDING",

    3: "STOP_PENDING",

    4: "RUNNING"

}


class SysCon(object):
    def start_service(self, service_name='GSUPService'):
        st = win32serviceutil.QueryServiceStatus(service_name)[1]
        if st == 4:
            print('当前服务%s的状态为:%s' % (service_name, status_code[st]))
            pass
        elif st == 2:
            print('当前服务%s 的状态为 %s' % (service_name, status_code[st]))
            pass
        elif st == 1:
            print('当前服务%s 的状态为： %s，开始启动服务' % (service_name, status_code[st]))
            win32serviceutil.StartService(service_name)
            print("服务启动成功")
        else:
            print('当前服务状态为：%s,需要手动启动' % status_code[st])
            pass
    
    def restart_service(self, service_name='GSUPService'):
        st = win32serviceutil.QueryServiceStatus(service_name)[1]
        if st == 4:
            win32serviceutil.StopService(service_name)
            time.sleep(2)
            win32serviceutil.StartService(service_name)
        elif st == 1:
            win32serviceutil.StartService(service_name)
        else:
            print('当前服务状态为：%s,需要手动启动' % status_code[st])
            pass

    def win_set_time_by_now(self, days=0):
    
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