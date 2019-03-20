#encoding:utf-8
from wxsearch import db,login_manager
from datetime import datetime

#用户类
class User(db.Model):
    id = db.Column(db.Integer , primary_key = True,autoincrement=True)
    username = db.Column(db.String(80),unique = True)
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))
    create_time = db.Column(db.DateTime)
    def __init__(self,username,password,salt=''):
        self.username = username
        self.password = password
        self.salt = salt
        self.create_time = datetime.now()

    def __repr__(self):
        return ('<User %d %s>' % (self.id, self.username)).encode('utf-8')

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id


class Article(db.Model):
    id = db.Column(db.Integer , primary_key = True,autoincrement=True)
    title = db.Column(db.Text,unique = True)
    url = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)

    def __init__(self,title,url,create_time):
        self.title = title
        self.url = url
        self.create_time = str(create_time)
    def __repr__(self):
        return (u'<User {0} {1} {2} >'.format(self.title,self.url,self.create_time)).encode('utf-8')

class Sear():

    def __init__(self,key,value):
        self.key = key
        self.value = value

    def add(self):
        self.value += 1


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)