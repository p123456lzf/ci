# -*- coding: utf-8 -*-
from config import db

class ci(db.Model):
    sn = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(64),unique=True)
    paragraphs = db.Column(db.String(1024),unique=True)
    rhythmic = db.Column(db.String(64),unique=True)

    def __init__(self, sn, author, paragraphs, rhythmic):
        self.sn = sn
        self.author = author
        self.paragraphs = paragraphs
        self.rhythmic = rhythmic

class user(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(64),unique=True)
    looked = db.Column(db.String(1024), unique=True)
    is_creating = db.Column(db.String(1024), unique=True)
    finished = db.Column(db.String(1024), unique=True)

    def __init__(self, user_id, user_name, looked, is_creating, finished):
        self.user_id = user_id
        self.user_name = user_name
        self.looked = looked
        self.is_creating = is_creating
        self.finished = finished

