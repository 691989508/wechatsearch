#encoding:utf-8

from wxsearch import app,db
from flask_script import Manager
from wxsearch.models import User,Article
import random
manager = Manager(app)


@manager.command
def init_database():
    pass
    # db.drop_all()
    # db.create_all()
    # for i in range(0,100):
    #     db.session.add(User('no.{}'.format(str(i+1)),'123456{}'.format(str(i+1)),'../static/touxiang/{}.jpeg'.format(random.randint(1,989))))
    # db.session.commit()
    #数据库查询
    #print len(list(set(Article.query.all())))
    # print 2,User.query.all()
    # print 3,Article.query.filter_by(id=5).first()
    # print Article.query.filter(Article.title.like('%一月%')).all()
    # print 4,User.query.order_by(User.id.desc()).offset(1).limit(2).all()
    # print 5,User.query.filter(User.userimage.endswith('jpeg')).limit(3).all()

    #print 6,Article.query.paginate(page=1,per_page=10).items
    #print User.query.limit(10).all()

    #数据库更新


if __name__ == '__main__':
    manager.run()












