# -*- coding: UTF-8 -*
'''
Created on 2018年11月23日

@author: Robin
'''

__version__ = '1.0.0'


def md5(s):
    import hashlib
    m2 = hashlib.md5()
    m2.update(s.encode("utf8"))
    return m2.hexdigest()


def get_sign(salt, key):
    salt = str(salt)
    key = str(key)
    return md5(md5(salt) + md5(key))


class App(object):
    '''用户应用'''

    def __init__(self, servurl, appid, appkey):
        '''创建需要应用'''
        self.servurl = servurl.rstrip('/')
        self.appid = appid
        self.appkey = appkey

    def doApi(self, apiname, data):
        import requests, json, time
        time = int(time.time())
        data['_appid'] = self.appid
        data['_time'] = time
        data['_sign'] = get_sign(time, self.appkey)

        url = '%s/iot/%s' % (self.servurl, apiname)
        headers = {"Content-Type": "application/json"}
        res = requests.post(url, data=json.dumps(data), headers=headers).json()
        if not res or res['code'] != 0:
            raise Exception('%s:%s' % (res.get('code', -1), res.get('msg', '')))
        return res


class DTU(object):
    def __init__(self, app, dtu_id):
        '''app: 应用对象  dtu_id:DTU的ID(字符串)'''
        self.app = app
        self.dtu_id = str(dtu_id)

    def updateDevices(self, devs):
        '''批量更新多个设备'''
        data = {
            'dtu_id': self.dtu_id,
            'devices': devs,
        }
        return self.app.doApi('update', data)

    def updateValues(self, dev_id, vals, time=None):
        '''批量更新单个设备的多个值。'''
        return self.updateDevices([{'dev_id': str(dev_id), 'attr': vals, 'time': time}])

    def updateValue(self, dev_id, attr_id, value, time=None):
        '''更新指定设备的指定值。dev_id:设备ID(字符串), attr_id:属性ID(字符串), value:属性值(任意Python类型)，time:时间戳(time.time()获取)'''
        return self.updateValues(dev_id, {str(attr_id): value}, time=time)


def test():
    # 需python requests包，如果没安装的话执行: pip install requests
    import random, time

    servurl = 'http://127.0.0.1:8080/'
    app = App(servurl, '1', '')

    # 创建DTU对象
    dtu = DTU(app, 'dtu1')

    # 更新指定设备的status属性
    while True:
        try:
            print(dtu.updateValue('dev2', 'v', int(random.random() * 4096), time.time()))  # 12 0-2095 -> 0-5
        except:
            import traceback
            traceback.print_exc()
        time.sleep(1)


if __name__ == '__main__':
    test()
