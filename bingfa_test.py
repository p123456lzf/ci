#! -*- coding:utf-8 -*-

import requests
import random
import time

urls = ['http://127.0.0.1:5000/yunjiao/火',
       'http://127.0.0.1:5000/pingze/火车卡死啦',
       'http://127.0.0.1:5000/rhythmic_rule/水调歌头',
       'http://127.0.0.1:5000/rhythmic/水调歌头',
       'http://127.0.0.1:5000/author/苏轼']

while True:
    t1 = time.time()
    print(t1)
    url = urls[random.randint(0,4)]
    res = requests.get(url).text
    dt = time.time() - t1
    print("耗时" + "%.2f秒" % dt)
    print(res)
    time.sleep(0.01)