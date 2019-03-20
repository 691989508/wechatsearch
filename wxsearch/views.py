#encoding:utf-8

from wxsearch import app,db
from flask import render_template,request,redirect,flash,get_flashed_messages
from models import User,Article,Sear
import json
import jieba
from collections import Counter
import random
import hashlib
from flask_login import login_user,logout_user,current_user,login_required

def search_url(search):
    '''搜索'''
    sear = jieba.cut(search.replace(' ', ''), cut_all=True)
    word_ = ' '
    word_ = word_.join(sear)
    words = word_.split(' ')
    out_puts = []
    for word in words:
        article_list = Article.query.filter(Article.title.like('%{}%'.format(word.encode('utf-8')))).order_by(Article.create_time.desc()).all()
        for article in article_list:
            out_puts.append((article.title,article.url,article.create_time))
    count = Counter(out_puts)
    count_dict = dict(count)
    newout = sorted(count_dict, key=count_dict.__getitem__, reverse=True)
    return newout


@app.route('/',methods={'post', 'get'})#, methods={'post', 'get'}
def index():

    last_page = int(len(Article.query.all())/10)
    articles = Article.query.order_by(Article.create_time.desc()).limit(10).all()
    return render_template('index.html',articles = articles,page = 1,last_page=last_page)


@app.route('/page/<int:page>/',methods={'post', 'get'})
@login_required
def next_page(page):
    page_num = len(Article.query.all())
    last_page = int(page_num/10)

    paginate = Article.query.order_by(Article.create_time.desc()).paginate(page=page,per_page=10,error_out=False)
    # map = {'has_next':paginate.has_next}
    # articles = []
    # for article in paginate.items:
    #     art = {'title':article.title, 'url':article.url}
    #     articles.append(art)
    # map['article'] = articles
    return render_template('page.html',articles = paginate.items,last_page=last_page,page=page)#json.dumps(map)#,render_template('page.html',articles = paginate.items)


@app.route('/search/',methods={'post', 'get'})#,
@login_required
def search():
    search = request.values.get('wd')

    if search == '':
        last_page = int(len(Article.query.all())/10)
        articles = Article.query.limit(20).all()
        return render_template('index.html',articles = articles,page = 1,last_page=last_page)
    else:
        articles = search_url(search)
        return render_template('search.html',articles = articles,search=search)


@app.route('/regloginpage/')
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.args.get('next'))



@app.route('/reg/',methods={'post', 'get'})
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名或密码不能为空', 'reglogin')
    user = User.query.filter_by(username=username).first()
    if user!=None:
        return redirect_with_msg('/regloginpage/', u"用户名已存在", 'reglogin')

    salt = '.'.join(random.sample('01234567890abcdefghigABCDEFGHI', 10))
    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    return render_template('login.html')


def redirect_with_msg(target,msg,catagory):
    if msg!=None:
        flash(msg,category=catagory)
        return redirect(target)


@app.route('/login/',methods={'post', 'get'})
def login():
    if request.method == 'POST':
        #"接受到数据"

        username = request.values.get('username').strip()
        password = request.values.get('password').strip()

        user = User.query.filter_by(username=username).first()
        if user == None:
            #"用户名不存在"
            return redirect_with_msg('/regloginpage/', u"用户名不存在",'reglogin')
        m = hashlib.md5()
        m.update(password + user.salt)

        if user.password!=m.hexdigest():
            #"密码错误"
            return redirect_with_msg('/regloginpage/', u"密码错误", 'reglogin')
        #"登录成功"
        login_user(user)
        next = request.values.get("next")
        print next
        if next != None and next != 'None':# and next.startswith('/'):
            return redirect(next)
        else:
            return redirect('/')
    return render_template('login.html',next=request.args.get("next"))


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/login/')