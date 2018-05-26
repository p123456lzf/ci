# -*- coding: utf-8 -*-
from config import app,db
from models import Ci,User,Finished,IsCreating
from get_pinyin import PinYin
from pingze import pingzes
import configparser
import datetime
#from gevent.wsgi import WSGIServer

@app.route('/')
def hello():
    return 'hello'

# 用于第一次登陆，如果此人是第一次登陆，则建库储存个人基本信息(ok为0表示此用户第一次登陆，为1表示老用户）
#  Done（无需异常处理）
@app.route('/user/<user_id>/name/<name>')
def setup_user(user_id,name):
    the_user = User.query.filter_by(user_id=user_id).first()
    if the_user == None:
        user = User(user_id=user_id, user_name=name, looked='', is_creating='', finished='')
        db.session.add(user)
        db.session.commit()
        results_json = "{\"ok\":0,\"data\":[{"
        results_json += "\"user_id\":" + "\"" + user_id + "\","
        results_json += "\"user_name\":" + "\"" + name + "\","
        results_json += "\"looked\":" + "\"\","
        results_json += "\"is_creating\":" + "\"\","
        results_json += "\"finished\":" + "\"\"}]}"
    else:
        results_json = "{\"ok\":1,\"data\":[{"
        results_json += "\"user_id\":" + "\"" + the_user.user_id + "\","
        results_json += "\"name\":" + "\"" + the_user.user_name + "\","
        results_json += "\"looked\":" + "\"" + the_user.looked + "\","
        results_json += "\"is_creating\":" + "\"" + the_user.is_creating + "\","
        results_json += "\"finished\":" + "\"" + the_user.finished + "\"}]}"
    return results_json

# 用于返回具体某个词 根据唯一标识这个词对应的id 同时储存用户id浏览记录
#  Done（无需异常处理）
@app.route('/user/<user_id>/poetry/<id>')
def get_poetry(user_id,id):
    results = Ci.query.filter_by(sn=id).first()
    results_json = "{\"data\":[{"
    results_json += "\"sn\":" + str(results.sn) + ","
    results_json += "\"author\":" + "\"" + results.author + "\","
    results_json += "\"paragraphs\":" + "\"" + results.paragraphs.replace("\"","'") + "\","
    results_json += "\"rhythmic\":" + "\"" + results.rhythmic + "\"}]}"
    the_user = User.query.filter_by(user_id=user_id).first()
    the_user_looked = the_user.looked
    if the_user_looked != None:
        the_user_looked_list = the_user_looked.split(',')
        on_off = 0
        for looked in the_user_looked_list:
            if looked == str(id):
                on_off = 1
                break
        if on_off == 0:
            the_user_looked = the_user.looked + str(id) + ','
            User.query.filter_by(user_id=user_id).update({'looked': the_user_looked})
    else:
        the_user_looked = the_user.looked + str(id) + ','
        User.query.filter_by(user_id=user_id).update({'looked': the_user_looked})
    db.session.commit()
    return results_json

# 根据诗人返回符合的词
#  Done（已异常处理）
@app.route('/author/<keyword>')
def poetry_find_by_author(keyword):
    results = Ci.query.filter(Ci.author.like("%" + keyword + "%")).all()
    results_json = "{\"data\":["
    i = 0
    for result in results:
        i += 1
        results_json += "{\"sn\":" + str(result.sn) + ","
        results_json += "\"author\":" + "\"" + result.author + "\","
        results_json += "\"paragraphs\":" + "\"" + result.paragraphs.replace("\"", "'") + "\","
        results_json += "\"rhythmic\":" + "\"" + result.rhythmic + "\"},"
    if i != 0:
        results_json = results_json[:-1] + "]," + "\"num\":" + str(i) + "}"
    else:
        results_json = results_json + "]," + "\"num\":" + str(i) + "}"
    return results_json

# 根据内容返回符合的词（！！！请搜索短句！！！可以优化，但需要时间，暂且不管）
#  Done（已异常处理）
@app.route('/paragraphs/<keyword>')
def poetry_find_by_paragraphs(keyword):
    results = Ci.query.filter(Ci.paragraphs.like("%" + keyword + "%")).all()
    results_json = "{\"data\":["
    i = 0
    for result in results:
        i += 1
        results_json += "{\"sn\":" + str(result.sn) + ","
        results_json += "\"author\":" + "\"" + result.author + "\","
        results_json += "\"paragraphs\":" + "\"" + result.paragraphs.replace("\"", "'") + "\","
        results_json += "\"rhythmic\":" + "\"" + result.rhythmic + "\"},"
    if i != 0:
        results_json = results_json[:-1] + "]," + "\"num\":" + str(i) + "}"
    else:
        results_json = results_json + "]," + "\"num\":" + str(i) + "}"
    return results_json

# 根据词牌返回符合的词
#  Done（已异常处理）
@app.route('/rhythmic/<keyword>')
def poetry_find_by_rhythmic(keyword):
    results = Ci.query.filter(Ci.rhythmic.like("%" + keyword + "%")).all()
    results_json = "{\"data\":["
    i = 0
    for result in results:
        i += 1
        results_json += "{\"sn\":" + str(result.sn) + ","
        results_json += "\"author\":" + "\"" + result.author + "\","
        results_json += "\"paragraphs\":" + "\"" + result.paragraphs.replace("\"", "'") + "\","
        results_json += "\"rhythmic\":" + "\"" + result.rhythmic + "\"},"
    if i != 0:
        results_json = results_json[:-1] + "]," + "\"num\":" + str(i) + "}"
    else:
        results_json = results_json + "]," + "\"num\":" + str(i) + "}"
    return results_json

# 根据用户名，词牌名，词的内容，进行储存(有字数限制 512个字，包含标点），赋予“我的创作”编号
#  Done（无需异常处理）
@app.route('/user/<user_id>/user_name/<name>/poetry/<words>/rhythmic/<rhythmic>')
def save_poetry(user_id,name,words,rhythmic):
    config=configparser.ConfigParser()
    config.read('config.ini')
    sn = int(config['info']['finished_sn'])
    config.set('info','finished_sn',str(sn+1))
    config.write(open('config.ini',"w"))
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.add(Finished(sn=sn,user_id=user_id,user_name=name,rhythmic=rhythmic,paragraphs=words,time=nowTime,comment=''))
    db.session.commit()
    the_user = User.query.filter_by(user_id=user_id).first()
    the_user_finished = the_user.finished
    if the_user_finished != None:
        the_user_finished = the_user.finished + str(sn) + ','
        User.query.filter_by(user_id=user_id).update({'finished': the_user_finished})
    else:
        the_user_finished = the_user.finished + str(sn) + ','
        User.query.filter_by(user_id=user_id).update({'finished': the_user_finished})
    db.session.commit()
    return "{\"ok\":1}"

# 储存评论，需要发表人的id以及被评论的id
#  Done（无需异常处理）
@app.route('/user_name/<name>/finished/<sn>/comment/<comment>')
def save_comments(name,sn,comment):
    finished = Finished.query.filter_by(sn=sn).first()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if finished.comment == None:
        comment_json = "{\"user_name\":\"" + name + "\"," + "\"comment\":\"" + comment + "\"," + "\"time\":\"" + nowTime + "\"},"
    else:
        comment_json = finished.comment + "{\"user_name\":\"" + name + "\"," + "\"comment\":\"" + comment + "\"," + "\"time\":\"" + nowTime + "\"},"
    Finished.query.filter_by(sn=sn).update({'comment': comment_json})
    db.session.commit()
    return "{\"ok\":1}"

# 根据用户名，词牌名，词的内容，进行储存(默认会储存新的创作）
#  Done（无需异常处理）
@app.route('/user/<user_id>/user_name/<name>/iscreating/<words>/rhythmic/<rhythmic>')
def save_iscreating(user_id,name,words,rhythmic):
    config = configparser.ConfigParser()
    config.read('config.ini')
    sn = int(config['info']['is_creating_sn'])
    config.set('info', 'is_creating_sn', str(sn + 1))
    config.write(open('config.ini', "w"))
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.session.add(
        IsCreating(sn=sn, user_id=user_id, user_name=name, rhythmic=rhythmic, paragraphs=words, time=nowTime))
    db.session.commit()
    the_user = User.query.filter_by(user_id=user_id).first()
    the_user_is_creating = the_user.is_creating
    if the_user_is_creating != None:
        the_user_is_creating = the_user.is_creating + str(sn) + ','
    else:
        the_user_is_creating = the_user.is_creating + str(sn) + ','
    User.query.filter_by(user_id=user_id).update({'is_creating': the_user_is_creating})
    db.session.commit()
    return "{\"ok\":1}"

# 根据完成作品编号返回对应作品
#  Done（无需异常处理）
@app.route('/finished/<sn>')
def poetry_find_by_finished_sn(sn):
    result = Finished.query.filter_by(sn=sn).first()
    results_json = "{\"data\":["
    results_json += "{\"sn\":" + str(result.sn) + ","
    results_json += "\"user_id\":" + "\"" + result.user_id + "\","
    results_json += "\"user_name\":" + "\"" + result.user_name + "\","
    results_json += "\"rhythmic\":" + "\"" + result.rhythmic + "\","
    results_json += "\"paragraphs\":" + "\"" + result.paragraphs + "\","
    results_json += "\"time\":" + "\"" + str(result.time) + "\","
    if result.comment == '':
        results_json += "\"comment\":[]"
    else:
        results_json += "\"comment\":[" + result.comment[:-1] + "]"
    results_json = results_json + "}]}"
    return results_json

# 根据正在创作作品编号返回对应作品
#  Done（无需异常处理）
@app.route('/iscreating/<sn>')
def poetry_find_by_iscreating(sn):
    result = IsCreating.query.filter_by(sn=sn).first()
    results_json = "{\"data\":["
    results_json += "{\"sn\":" + str(result.sn) + ","
    results_json += "\"user_id\":" + "\"" + result.user_id + "\","
    results_json += "\"user_name\":" + "\"" + result.user_name + "\","
    results_json += "\"rhythmic\":" + "\"" + result.rhythmic + "\","
    results_json += "\"paragraphs\":" + "\"" + result.paragraphs + "\","
    results_json += "\"time\":" + "\"" + str(result.time) + "\"}]}"
    return results_json

# 根据word 返回这个字对应的平仄
#  Done（已异常处理）
@app.route('/pingze/<words>')
def get_pingze(words):
    try:
        test = PinYin()
        test.load_word()
        results = test.hanzi2yindiao(string=words)
        pz = []
        for result in results:
            x1, x2, x3 = 0, 0, 0
            for i in result:
                if i == '1' or i == '2':
                    x1 = 1
                    continue
                if i == '3' or i == '4':
                    x2 = 1
                    continue
                if i == '5':
                    x1 = 1
                    x2 = 1
                    continue
                x3 = 1
            if x1 == 1 and x2 == 1:
                pz.append('中')
                continue
            if x1 == 1 and x2 == 0:
                pz.append('平')
                continue
            if x1 == 0 and x2 == 1:
                pz.append('仄')
                continue
            if x3 == 1:
                pz.append('空')
        result_json = "{\"ok\":1,\"result\":\"" + str(pz) + "\"}"
    except:
        result_json = "{\"ok\":0,\"}"
    return result_json

# 根据words 返回这些字是否韵脚相同 并返回对应的韵脚推荐(返回{"ok":0}表示韵脚不统一，或者多音字不确定韵脚，若统一则返回推荐韵脚）
#  Done（已异常处理）
@app.route('/yunjiao/<words>')
def get_yunjiao(words):
    try:
        test = PinYin()
        test.load_word()
        results = test.hanzi2yunjiao(string=words)
        for index, item in enumerate(results):
            if index == 0:
                first_yj = item
            else:
                ok = 0
                for i in item:
                    if i in first_yj:
                        first_yj = [i]
                        ok = 1
                if ok == 0:
                    return "{\"ok\":0,\"suggestion\":\"[]\"}"
        if len(first_yj) == 1:
            suggestion = test.get_yunjiao(first_yj[0])
            return "{\"ok\":1,\"suggestion\":\"" + str(suggestion) + "\"}"
        else:
            return "{\"ok\":0,\"suggestion\":\"" + str(first_yj) + "\"}"
    except:
        return "{\"ok\":0}"

# 根据词牌名返回词牌对应格式
#  Done（已异常处理）
@app.route('/rhythmic_rule/<keyword>')
def get_rhythmic_rule(keyword):
    keys = [x for x in pingzes.items() if keyword in x[0]]
    num = 0
    result_json = "{\"ok\":1,\"data\":["
    for key in keys:
        num += 1
        result_json += "{\"rhythmic\":\"" + key[0] + "\",\"rule\":\"" + key[1] + "\"},"
    result_json =result_json[:-1] + "],\"num\":" + str(num) + "}"
    if num == 0:
        result_json = "{\"ok\":0,\"num\":0}"
    return result_json

@app.route('/.well-known/pki-validation/fileauth.txt')
def a():
    return "201805251248352o1epww13e43x6rfnbdoqh1dku5r9p4bfjipiyb389y7ba6bid"


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,ssl_context=('www.ikjmls.cn.crt', 'www.ikjmls.cn.key'))
    #WSGIServer(('0.0.0.0', 80), app).serve_forever()