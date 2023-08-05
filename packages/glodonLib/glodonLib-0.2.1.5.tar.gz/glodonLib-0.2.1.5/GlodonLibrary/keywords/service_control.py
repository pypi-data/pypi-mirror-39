# coding:utf-8

import time
import os
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


class SysCon:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
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

    def run_program(self, pg, params="", fdir="", isAdmin=False):
        """
        windows 执行命令，并返回子进程的返回值
        :param pg: 要打开的程序
        :param params: 传递给要打开程序的参数，默认为空
        :param fdir: 执行程序所在的目录，如果已经在跟目录，默认为空
        :return:
        """
        global r
        import subprocess
        if fdir != '':
            pg = os.path.join(fdir, pg)
        if isAdmin:
            r = subprocess.Popen('sudo  %s %s' % (pg, params), stdout=subprocess.PIPE, shell=True)
        else:
            r = subprocess.Popen(['CMD', '/C', pg, params], stdout=subprocess.PIPE)
    
        return r.wait()


if __name__ == '__main__':
    pass