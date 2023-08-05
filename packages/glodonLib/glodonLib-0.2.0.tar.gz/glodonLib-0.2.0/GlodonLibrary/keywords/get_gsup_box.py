# coding=utf-8
import _winreg
import base64
import json
from functools import wraps


import requests

__all__ = ['run_program', 'GetBoxParams','read_last_line']


def _add_local_params(func):
    @wraps(func)
    def wras(self):
        version = QueryRegValue(sub_key=r'Software\Glodon\GDraw\1.0').get_value('Version')
        self.params['oldversion'] = version
        devid = QueryRegValue().get_guid()
        self.params['devid'] = devid
        func(self, devid, version)

    return wras


def read_last_line(rfile, n):
    with open(rfile, 'r') as f:
        txt = f.readlines()
    keys = [k for k in range(0, len(txt))]
    result = {k: v for k, v in zip(keys, txt[::-1])}
    for i in range(n):
        if 'return code'in result[i]:
            return result[i]


class QueryRegValue(object):
    def __init__(self, key=_winreg.HKEY_LOCAL_MACHINE, sub_key=r'Software\Wow6432Node\Glodon\GDP\2.0'):
        self.handle = _winreg.OpenKey(key, sub_key)
        self._sub_key =sub_key
        
    def get_guid(self):
        if self._sub_key == r'Software\Wow6432Node\Glodon\GDP\2.0':
            return _winreg.QueryValueEx(self.handle, 'guid')[0].decode('utf-8')
        else:
            raise Exception('get deviceid wrong,please check sub_key!')
    
    def get_value(self, key):
        
        return _winreg.QueryValueEx(self.handle, key)[0].decode('utf-8')
    
    def get_gsup_verison(self):
        if self._sub_key == r'Software\Wow6432Node\Glodon\GDP\2.0':
            return _winreg.QueryValueEx(self.handle, 'Version')[0].encode('utf-8')
        else:
            raise Exception('get gsup version wrong,please check sub_key!')


class GetBoxParams(object):
    def __init__(self, env='cs'):
        self.params = dict()
        if env == 'cs':
            self.base_url = 'http://gsup-test.glodon.com/'
            self.product = '153'
        elif env == 'sc':
            self.product = '1'
            self.base_url = 'http://gsup.glodon.com/'
    
    def _products_gdraw_params(self):
        url = self.base_url + 'api/v2/products?secret=false'
        resp = requests.get(url)
   
        products = resp.json()['info']['products']
        for item in products:
            if item['clientid'] == 'GDraw':
                self.params['exe'] = item['exe']
                self.params['logo'] = item['logo']
                self.params['showname'] = item['showname']
                self.params['optional'] = item['optional']
                self.params['clientid'] = item['clientid']
                self.params['path'] = item['path']
                break
    
    @_add_local_params
    def _record_gdraw_params(self, devid, ver):
  
        url = self.base_url + 'api/v2/record?secret=false'
        
        data = {
            "product": self.product,
            "deviceid": devid,
            "version": ver,
            "bits": "64",
            "os": 'Win7',
            "sysbits": "64",
            "updateid": "74001"
        }
        resp = requests.post(url, params=data)

        assert resp.json()['status'] != 5000, "没有要查询升级的产品的信息！"
        infos = resp.json()['info']
        for k, v in infos.items():
            if k == 'product_id':
                self.params['pid'] = infos[k]
                del infos[k]
            if k == 'name':
                self.params['fname'] = r'C:\ProgramData\Glodon\GSUP\download\%s' % infos[k]
                del infos[k]
            if k == 'full_update':
                self.params['diff'] = infos[k]
                del infos[k]
            if k == 'utype':
                if infos[k] == 1 or infos[k] == 0:
                    self.params['force'] = '0'
                elif infos[k] == 2:
                    self.params['force'] = '1'
                del infos[k]
            if k in ('can_update', 'ntype', 'args', 'message'):
                del infos[k]
        self.params['span'] = 'false'
        self.params.update(infos)
        
    def get_box_params(self, ischeck='false'):
        """
        
        :param ischeck: 是否为检查升级，有两种类型true和false，默认值为false。
        :return:
        """
        if ischeck == 'false':
            self.params['check'] = 'false'
        elif ischeck == 'true':
            self.params['check'] = 'true'
        else:
            raise ValueError('params wrong!')
        self._products_gdraw_params()
        self._record_gdraw_params()
        return self.params


def run_program(pg, params="", fdir="", isAdmin=False):
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
    # import subprocess,time
    import os
    s = GetBoxParams('cs').get_box_params()
    p = base64.b64encode(json.dumps(s))
    e = r'C:\\Program Files (x86)\\Common Files\\Glodon Shared\\GDP\\2.10.0.1711\\x86'
    return_code = run_program('gupdatebox.exe', p, e)
    print return_code
    # run_program('python', 'test02.py', '', True)
