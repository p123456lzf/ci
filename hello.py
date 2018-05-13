# -*- coding: utf-8 -*-
from config import app,db
from models import ci,user

@app.route('/')
def hello():
    return 'hello'

@app.route('/user/<user_id>/poetry/<id>')   #用于返回具体某个词 根据唯一标识这个词对应的id 同时储存用户id浏览记录 Done
def get_poetry(user_id,id):
    results = ci.query.filter_by(sn=id).first()
    results_json = "{\"data\":[{"
    results_json += "\"sn\":" + str(results.sn) + ","
    results_json += "\"author\":" + "\"" + results.author + "\","
    results_json += "\"paragraphs\":" + "\"" + results.paragraphs.replace("\"","'") + "\","
    results_json += "\"rhythmic\":" + "\"" + results.rhythmic + "\"}]}"
    the_user = user.query.filter_by(user_id=user_id).first()
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
            user.query.filter_by(user_id=user_id).update({'looked': the_user_looked})
    else:
        the_user_looked = the_user.looked + str(id) + ','
        user.query.filter_by(user_id=user_id).update({'looked': the_user_looked})
    db.session.commit()
    return results_json

@app.route('/pingze/<word>')   #根据word 返回这个字对应的平仄
def get_pingze(word):
    return word

@app.route('/yunjiao/<word>')   #根据word 返回这个字对应的合适的韵脚
def get_yunjiao(word):
    return word

@app.route('/user/<user_id>/poetry/<id>/comment/<comment>')   #储存评论，需要发表人的id以及被评论的id
def save_comments(user_id,id):
    return id

@app.route('/user/<user_id>/poetry/<words>/cipai/<cipai>')   #根据用户名，词牌名，词的内容，进行储存
def save_poetry(user_id,words,cipai):
    return True

@app.route('/user/<user_id>/iswriting/<words>/cipai/<cipai>')   #根据用户名，词牌名，词的内容，进行储存
def save_iswriting(user_id,words,cipai):
    return True

@app.route('/keyword/<keyword>')            #根据用户关键词进行搜索，返回符合的词
def poetry_find_by_keyword(keyword):
    return keyword

if __name__ == "__main__":
    #print(into_flash_str(4201587825642984))
    app.run()
    #, ssl_context=("ssl.crt","ssl.key")