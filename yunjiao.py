import re

with open("yunjiao.data",encoding='utf-8') as f:
    string = f.read()
    string = string.replace('\n','')
    a = string.split('篇')
    x = 0
    yunmu = {}
    yunjiao = {}
    for i in a:
        if x == 0:
            x = 1
            for j in re.findall(r'[a-zA-Z]+', i)[:-1]:
                yunmu[j] = 'a'
            yunjiao['a'] = str(re.findall(r'[\u4e00-\u9fa5]', i))
            xx = re.findall(r'[a-zA-Z]+', i)[-1]
        else:
            for j in re.findall(r'[a-zA-Z]+', i)[:-1]:
                yunmu[j.lower()] = xx
            yunjiao[xx] = str(re.findall(r'[\u4e00-\u9fa5]', i))
            xx = re.findall(r'[a-zA-Z]+', i)[-1]

if __name__ == "__main__":
    print(str(yunmu))
    print(str(yunjiao))