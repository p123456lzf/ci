# -*- coding: utf-8 -*-
from config import db

class Ci(db.Model):
    sn = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(63),unique=False)
    paragraphs = db.Column(db.String(1023),unique=False)
    rhythmic = db.Column(db.String(63),unique=False)

    def __init__(self, sn, author, paragraphs, rhythmic):
        self.sn = sn
        self.author = author
        self.paragraphs = paragraphs
        self.rhythmic = rhythmic

class User(db.Model):
    user_id = db.Column(db.String(63),primary_key=True)
    user_name = db.Column(db.String(63),unique=False)
    looked = db.Column(db.String(1023), unique=False)
    is_creating = db.Column(db.String(1023), unique=False)
    finished = db.Column(db.String(1023), unique=False)

    def __init__(self, user_id, user_name, looked, is_creating, finished):
        self.user_id = user_id
        self.user_name = user_name
        self.looked = looked
        self.is_creating = is_creating
        self.finished = finished

class Finished(db.Model):
    sn = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.String(63),unique=False)
    user_name = db.Column(db.String(63),unique=False)
    rhythmic = db.Column(db.String(63),unique=False)
    paragraphs = db.Column(db.String(1023),unique=False)
    time = db.Column(db.DateTime,unique=False)
    comment = db.Column(db.String(255),unique=False)

    def __init__(self, sn, user_id, user_name, rhythmic, paragraphs, time, comment):
        self.sn = sn
        self.user_id = user_id
        self.user_name = user_name
        self.rhythmic = rhythmic
        self.paragraphs = paragraphs
        self.time = time
        self.comment = comment

class IsCreating(db.Model):
    sn = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.String(63),unique=False)
    user_name = db.Column(db.String(63),unique=False)
    rhythmic = db.Column(db.String(63),unique=False)
    paragraphs = db.Column(db.String(1023),unique=False)
    time = db.Column(db.DateTime,unique=False)
#    comment = db.Column(db.String(255),unique=True)

    def __init__(self, sn, user_id, user_name, rhythmic, paragraphs, time):
        self.sn = sn
        self.user_id = user_id
        self.user_name = user_name
        self.rhythmic = rhythmic
        self.paragraphs = paragraphs
        self.time = time
#        self.comment = comment

if __name__ == "__main__":
    db.create_all()
