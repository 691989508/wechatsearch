#encoding:utf-8


import MySQLdb
import jieba
import jieba.analyse
from collections import Counter
class Sear():

    def __init__(self,key,value):
        self.key = key
        self.value = value

    def add(self):
        self.value += 1

class Article():

    def __init__(self,title,url,create_time):

        self.title = title
        self.url = url
        self.create_time = create_time

def search_url(search,art):
    '''搜索'''

    search_list = search.split(' ')
    article_list = art
    output_text_list = []



    for search_val in search_list:
        for atitle in article_list:
            if search_val in atitle.title:
                notexistence = True
                for out in output_text_list:
                    if atitle.title == out.key.title:
                        notexistence = False
                        out.add()
                if notexistence:
                    se = Sear(atitle,1)
                    output_text_list.append(se)

    sort_list = sorted(output_text_list, key=lambda Sear: Sear.value, reverse=True)


    return sort_list


if __name__ == '__main__':


    dbpool = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='tieba', charset='utf8',
                             use_unicode=False)
    cursor = dbpool.cursor()
    # sql2 = """select id,title from article"""
    # cursor.execute(sql2)
    # articles = cursor.fetchall()
    # out = []
    # for ar in articles:
    #     a = Article(ar[0],ar[1])
    #     out.append(a)
    # for i in out:
    #     sql3 = """select title from article where title={}""".format(i.title)
    #     cursor.execute(sql3)

    # out = list(set(articles))
    # print len(out)
    # for i,ti in articles:
    #     if i<1:
    #         out.append(ti)
    #     else:
    #         if ti in out:
    #             continue
    #         else:
    #             out.append(ti)
    # sql3 = """CREATE TABLE article (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,title TEXT UNION,url CHAR(255),create_time"""
    # cursor.execute(sql3)



    # t1 = [u"狐金 黑盒子 喵哥",u'狐金 黑盒子 喵哥',u"一代金/狐金/龙女金/猪金/蝶金/鸡金/考金/猴红/鸡红八红"]
    #
    keyword = "狐金 黑盒子 喵哥"
    s2 = jieba.cut(keyword.replace(' ',''),cut_all=True)
    word = ' '
    word = word.join(s2)
    print word
    words = word.split(' ')
    out_puts = []
    for word in words:
        sql2 = """select DISTINCT title,url,create_time from article where title like '%{}%'""".format(word.encode('utf-8'))
        cursor.execute(sql2)
        articles = cursor.fetchall()
        for article in articles:
            out_puts.append((article[0],article[1],article[2]))
    count = Counter(out_puts)
    count_dict = dict(count)
    print(type(count_dict))
    for k in sorted(count_dict, key=count_dict.__getitem__, reverse=True):
        print k[0], count_dict[k]














    # for key,value in count_dict.items():
    #     print key,value


    #         if len(out_puts)<1:
    #             sear = Sear(article[0], 0)
    #             out_puts.append(sear)
    #         else:
    #             val = True
    #             for out in out_puts:
    #                 print(out.key)
    #                 if article[0]==out.key:
    #                     out.add()
    #                     val = False
    #                     break
    #             if val:
    #                 sear = Sear(article[0],0)
    #                 out_puts.append(sear)
    #                 print len(out_puts)
    # print len(out_puts)
    # sort_list = sorted(out_puts, key=lambda Sear: Sear.value, reverse=True)
    # for out in sort_list:
    #     print out.value,out.key
    #


    #sql_select = """SELECT title,id FROM article"""
    #cursor.execute(sql_select)
    # art_list = []
    # for article in articles:
    #     ar = Article(article[0].decode('utf-8'),article[1])
    #     art_list.append(ar)
    # search = u'狐金 黑盒子 喵哥'
    # sa = search_url(search,art_list)
    # for a in sa:
    #     print a.key.title,a.value
    dbpool.commit()
    dbpool.close()



