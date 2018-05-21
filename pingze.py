import re

with open("pingze.data",encoding='utf-8') as f:
    string = f.read()
    pingze = re.findall(r'．.*\n[平,仄,中,，,。,\n,、]+',string)
    pingzes = {}
    xx = 0
    for i in pingze:
        x = i.replace('\n','')
        name = re.findall(r'.+?[中,平,仄]', x[1:])[0][:-1]
        rule = re.findall(r'[平,仄,中,，,。,、]+', x[1:])[0]
        pingzes[name] = rule
        xx += 1
if __name__ == "__main__":
    print(pingzes)
    print(str(xx))