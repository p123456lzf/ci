#! -*- coding:utf-8 -*-

import requests
import random
import time

urls = ['http://127.0.0.1:5000/author/苏轼']

while True:
    t1 = time.time()
    print(t1)
    res = requests.get(urls[0]).text
    dt = time.time() - t1
    print("耗时" + "%.2f秒" % dt)
    time.sleep(0.01)