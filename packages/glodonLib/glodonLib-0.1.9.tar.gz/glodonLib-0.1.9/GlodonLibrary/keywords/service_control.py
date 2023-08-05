# coding:utf-8

import time
import win32serviceutil

__all__ = ['start_service', 'restart_service']


status_code = {

    0: "UNKNOWN",

    1: "STOPPED",

    2: "START_PENDING",

    3: "STOP_PENDING",

    4: "RUNNING"

}


def start_service(service_name='GSUPService'):
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


def restart_service(service_name='GSUPService'):
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


if __name__ == '__main__':
    restart_service()