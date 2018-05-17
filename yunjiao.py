import re

with open("yunjiao.data",encoding='utf-8') as f:
    string = f.read()
    string = string.replace('\n','')
    a = string.split('篇')
    x = 0
    result1 = {}
    result2 = {}
    for i in a:
        if x == 0:
            x = 1
            for j in re.findall(r'[a-zA-Z]+', i)[:-1]:
                result1[j] = 'a'
            result2['a'] = str(re.findall(r'[\u4e00-\u9fa5]', i))
            xx = re.findall(r'[a-zA-Z]+', i)[-1]
        else:
            for j in re.findall(r'[a-zA-Z]+', i)[:-1]:
                result1[j.lower()] = xx
            result2[xx] = str(re.findall(r'[\u4e00-\u9fa5]', i))
            xx = re.findall(r'[a-zA-Z]+', i)[-1]