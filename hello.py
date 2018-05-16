# -*- coding: utf-8 -*-
from config import app,db
from models import Ci,User

@app.route('/')
def hello():
    return 'hello'

# 用于第一次登陆，如果此人是第一次登陆，则建库储存个人基本信息(ok为0表示此用户第一次登陆，为1表示老用户）
#  Done
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
#  Done
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
#  Done
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
#  Done
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
#  Done
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

# 储存评论，需要发表人的id以及被评论的id
@app.route('/user/<user_id>/poetry/<id>/comment/<comment>')
def save_comments(user_id,id):
    return id

# 根据用户名，词牌名，词的内容，进行储存
@app.route('/user/<user_id>/poetry/<words>/cipai/<cipai>')
def save_poetry(user_id,words,cipai):
    return True

# 根据用户名，词牌名，词的内容，进行储存
@app.route('/user/<user_id>/iswriting/<words>/cipai/<cipai>')
def save_iswriting(user_id,words,cipai):
    return True

# 根据word 返回这个字对应的平仄
@app.route('/pingze/<word>')
def get_pingze(word):
    return word

# 根据word 返回这个字对应的合适的韵脚
@app.route('/yunjiao/<word>')
def get_yunjiao(word):
    return word


if __name__ == "__main__":
    #print(into_flash_str(4201587825642984))
    app.run()
    #, ssl_context=("ssl.crt","ssl.key")